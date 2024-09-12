#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1/f noise correction from supreme-SPOON by Michael Radica

Made self-contained for use in ahsoka

"""

import numpy as np
import glob
import warnings
import bottleneck as bn
from tqdm import tqdm
from scipy.ndimage import median_filter
from astropy.io import fits

from jwst import datamodels




class OneOverFStep:
    """Wrapper around custom 1/f Correction Step.
    """

    def __init__(self, input_data, baseline_ints, output_dir='./',
                 smoothed_wlc=None, outlier_maps=None, trace_mask=None,
                 background=None, occultation_type='transit', exposure_type='nrs1'):
        """Step initializer.
        """

        self.tag = 'oneoverfstep.fits'
        self.output_dir = output_dir
        self.baseline_ints = baseline_ints
        self.smoothed_wlc = smoothed_wlc
        self.trace_mask = trace_mask
        self.outlier_maps = outlier_maps
        self.background = background
        self.occultation_type = occultation_type
        self.exposure_type = exposure_type
        self.datafiles = np.atleast_1d(input_data)
        self.fileroots = get_filename_root(self.datafiles)

    def run(self, even_odd_rows=True, save_results=True, force_redo=False):
        """Method to run the step.
        """

        all_files = glob.glob(self.output_dir + '*')
        do_step = 1
        results = []
        for i in range(len(self.datafiles)):
            # If an output file for this segment already exists, skip the step.
            expected_file = self.output_dir + self.fileroots[i] + self.tag
            if expected_file not in all_files:
                do_step = 0
                break
            else:
                results.append(datamodels.open(expected_file))
        if do_step == 1 and force_redo is False:
            print('Output files already exist.')
            print('Skipping 1/f Correction Step.\n')
        # If no output files are detected, run the step.
        else:
            results = oneoverfstep(self.datafiles,
                                   baseline_ints=self.baseline_ints,
                                   even_odd_rows=even_odd_rows,
                                   background=self.background,
                                   smoothed_wlc=self.smoothed_wlc,
                                   output_dir=self.output_dir,
                                   save_results=save_results,
                                   outlier_maps=self.outlier_maps,
                                   trace_mask=self.trace_mask,
                                   fileroots=self.fileroots,
                                   occultation_type=self.occultation_type,
                                   exposure_type=self.exposure_type)

        return results

def oneoverfstep(datafiles, baseline_ints, even_odd_rows=True,
                 background=None, smoothed_wlc=None, output_dir='./',
                 save_results=True, outlier_maps=None, trace_mask=None,
                 fileroots=None, occultation_type='transit', exposure_type='CLEAR'):
    """Custom 1/f correction routine to be applied at the group level. A
    median stack is constructed using all out-of-transit integrations and
    subtracted from each individual integration. The column-wise median of
    this difference image is then subtracted from the original frame to
    correct 1/f noise. Outlier pixels, background contaminants, and the target
    trace itself can (should) be masked to improve the estimation.

    Parameters
    ----------
    datafiles : array-like[str], array-like[RampModel], array-like[CubeModel]
        List of paths to data files, or RampModels themselves for each segment
        of the TSO. Should be 4D ramps, but 3D rate files can also be accepted.
    baseline_ints : array-like[int]
        Integration numbers of ingress and egress.
    even_odd_rows : bool
        If True, calculate 1/f noise seperately for even and odd numbered rows.
    background : str, array-like[float], None
        Model of background flux.
    smoothed_wlc : array-like[float], None
        Estimate of the normalized light curve.
    output_dir : str
        Directory to which to save results.
    save_results : bool
        If True, save results to disk.
    outlier_maps : array-like[str], None
        List of paths to outlier maps for each data segment. Can be
        3D (nints, dimy, dimx), or 2D (dimy, dimx) files.
    trace_mask : str, None
        Path to file containing a trace mask. Should be 3D (norder, dimy,
        dimx), or 2D (dimy, dimx).
    fileroots : array-like[str], None
        Root names for output files.
    occultation_type : str
        Type of occultation, either 'transit' or 'eclipse'.

    Returns
    -------
    corrected_rampmodels : array-like
        RampModels for each segment, corrected for 1/f noise.
    """

    print('Starting 1/f correction step.')

    # Output directory formatting.
    if output_dir is not None:
        if output_dir[-1] != '/':
            output_dir += '/'

    # Format the baseline frames - either out-of-transit or in-eclipse.
    baseline_ints = format_out_frames(baseline_ints,
                                            occultation_type)

    datafiles = np.atleast_1d(datafiles)
    # If outlier maps are passed, ensure that there is one for each segment.
    if outlier_maps is not None:
        outlier_maps = np.atleast_1d(outlier_maps)
        if len(outlier_maps) == 1:
            outlier_maps = [outlier_maps[0] for d in datafiles]

    data = []
    # Load in datamodels from all segments.
    for i, file in enumerate(datafiles):
        currentfile = open_filetype(file)
        data.append(currentfile)
        # To create the deepstack, join all segments together.
        if i == 0:
            cube = currentfile.data
        else:
            cube = np.concatenate([cube, currentfile.data], axis=0)

    # Generate the 3D deep stack (ngroup, dimy, dimx) using only
    # baseline integrations.
    msg = 'Generating a deep stack for each frame using baseline' \
          ' integrations...'
    print(msg)
    deepstack = make_deepstack(cube[baseline_ints])

    # In order to subtract off the trace as completely as possible, the median
    # stack must be scaled, via the transit curve, to the flux level of each
    # integration.
    # If no lightcurve is provided, estimate it from the current data.

    if smoothed_wlc is None:
        postage = cube[:, -1, 20:60, 1500:1550]
        timeseries = np.nansum(postage, axis=(1, 2))
        timeseries = timeseries / np.nanmedian(timeseries[baseline_ints])
        if exposure_type == 'CLEAR':
            # Smooth the time series on a timescale of roughly 2%.
            smoothed_wlc = median_filter(timeseries,
                                     int(0.02*np.shape(cube)[0]))
        else:
            smoothed_wlc = timeseries / timeseries
            

    # Background must be subtracted to accurately subtract off the target
    # trace and isolate 1/f noise. However, the background flux must also be
    # corrected for non-linearity. Therefore, it should be added back after
    # the 1/f is subtracted to be re-subtracted later.
    #if background is not None:
    #    if isinstance(background, str):
    #        background = np.load(background)

    # Individually treat each segment.
    corrected_rampmodels = []
    current_int = 0
    for n, datamodel in enumerate(data):
        print('Starting segment {} of {}.'.format(n + 1, len(data)))

        # Define the readout setup - can be 4D (recommended) or 3D.
        if np.ndim(datamodel.data) == 4:
            nint, ngroup, dimy, dimx = np.shape(datamodel.data)
        else:
            nint, dimy, dimx = np.shape(datamodel.data)

        # Read in the outlier map - a (nints, dimy, dimx) 3D cube
        if outlier_maps is None:
            print(' No outlier maps passed, ignoring outliers.')
            outliers = np.zeros((nint, dimy, dimx))
        else:
            print(' Using outlier map {}'.format(outlier_maps[n]))
            outliers = fits.getdata(outlier_maps[n])
            # If the outlier map is 2D (dimy, dimx) extend to int dimension.
            if np.ndim(outliers) == 2:
                outliers = np.repeat(outliers, nint)
                outliers = outliers.reshape((dimy, dimx, nint))
                outliers = outliers.transpose(2, 0, 1)
        # The outlier map is 0 where good and >0 otherwise. As this will be
        # applied multiplicatively, replace 0s with 1s and others with NaNs.
        outliers = np.where(outliers == 0, 1, np.nan)

        # Read in the main trace mask - a (dimy, dimx) or (3, dimy, dimx)
        # data frame.
        if trace_mask is None:
            print(' No trace mask passed, ignoring the trace.')
            tracemask = np.zeros((3, dimy, dimx))
        else:
            print(' Using trace mask {}.'.format(trace_mask))
            if isinstance(trace_mask, str):
                tracemask = fits.getdata(trace_mask)
            else:
                msg = 'Unrecognized trace_mask file type: {}.' \
                      'Ignoring the trace mask.'.format(type(trace_mask))
                warnings.warn(msg)
                tracemask = np.zeros((3, dimy, dimx))
        # Trace mask may be order specific, or all order combined. Collapse
        # into a combined mask.
        if np.ndim(tracemask) == 3:
            tracemask = tracemask[0].astype(bool) | tracemask[1].astype(bool)\
                        | tracemask[2].astype(bool)
        else:
            tracemask = tracemask
        # Convert into a multiplicative mask of 1s and NaNs.
        tracemask = np.where(tracemask == 0, 1, np.nan)
        # Reshape into (nints, dimy, dimx) format.
        tracemask = np.repeat(tracemask, nint).reshape((dimy, dimx, nint))
        tracemask = tracemask.transpose(2, 0, 1)
        # Combine the two masks.
        outliers = (outliers + tracemask) // 2

        # Initialize output storage arrays.
        corr_data = np.copy(datamodel.data)
        # Loop over all integrations to determine the 1/f noise level via a
        # difference image, and correct it.
        for i in tqdm(range(nint)):
            # i counts ints in this particular segment, whereas ii counts
            # ints from the start of the exposure.
            ii = current_int + i
            # Create the difference image.
            sub = datamodel.data[i] - deepstack * smoothed_wlc[ii]
            # Since the variable upon which 1/f noise depends is time, treat
            # each group individually.
            # Apply the outlier mask.
            sub *= outliers[i, :, :]
            # FULL frame uses multiple amplifiers and probably has to be
            # treated differently.
            if datamodel.meta.subarray.name == 'FULL':
                raise NotImplementedError
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', category=RuntimeWarning)
                if even_odd_rows is True:
                    # Calculate 1/f scaling seperately for even and odd
                    # rows. This should be taken care of by the RefPixStep,
                    # but it doesn't hurt to do it again.
                    dc = np.zeros_like(sub)
                    # For group-level corrections.
                    if np.ndim(datamodel.data == 4):
                        dc[:, ::2] = bn.nanmedian(sub[:, ::2], axis=1)[:, None, :]
                        dc[:, 1::2] = bn.nanmedian(sub[:, 1::2], axis=1)[:, None, :]
                    # For integration-level corrections.
                    else:
                        dc[::2] = bn.nanmedian(sub[::2], axis=0)[None, :]
                        dc[1::2] = bn.nanmedian(sub[1::2], axis=0)[None, :]
                else:
                    # Single 1/f scaling for all rows.
                    dc = np.zeros_like(sub)
                    # For group-level corrections.
                    if np.ndim(datamodel.data == 4):
                        dc[:, :, :] = bn.nanmedian(sub, axis=1)[:, None, :]
                    # For integration-level corrections.
                    else:
                        dc[:, :] = bn.nanmedian(sub, axis=0)[None, :]
            # Make sure no NaNs are in the DC map
            dc = np.where(np.isfinite(dc), dc, 0)
            corr_data[i] -= dc
        current_int += nint

        # Add back the zodi background.
        if background is not None:
            corr_data += background

        # Store results.
        rampmodel_corr = datamodel.copy()
        rampmodel_corr.data = corr_data
        corrected_rampmodels.append(rampmodel_corr)

        # Save the results if requested.
        if save_results is True:
            suffix = 'oneoverfstep.fits'
            rampmodel_corr.write(output_dir + fileroots[n] + suffix)

        # Close datamodel for current segment.
        datamodel.close()

    return corrected_rampmodels

def get_filename_root(datafiles):
    """Get the file name roots for each segment.

    Parameters
    ----------
    datafiles : array-like[str], array-like[jwst.datamodel]
        Datamodels, or paths to datamodels for each segment.

    Returns
    -------
    fileroots : array-like[str]
        List of file name roots.
    """

    fileroots = []
    for file in datafiles:
        # Open the datamodel.
        if isinstance(file, str):
            data = datamodels.open(file)
            filename = data.meta.filename
            data.close()
        else:
            filename = file.meta.filename
        # Get the last part of the path, and split file name into chunks.
        filename_split = filename.split('/')[-1].split('_')
        fileroot = ''
        # Get the filename before the step info and save.
        for chunk in filename_split[:-1]:
            fileroot += chunk + '_'
        fileroots.append(fileroot)

    return fileroots

def format_out_frames(out_frames, occultation_type='transit'):
    """Create a mask of baseline flux frames for lightcurve normalization.
    Either out-of-transit integrations for transits or in-eclipse integrations
    for eclipses.

    Parameters
    ----------
    out_frames : array-like[int]
        Integration numbers of ingress and egress.
    occultation_type : str
        Type of occultation, either 'transit', 'eclipse', or 'phase curve'.

    Returns
    -------
    baseline_ints : array-like[int]
        Array of out-of-transit, or in-eclipse frames for transits and
        eclipses respectively.

    Raises
    ------
    ValueError
        If an unknown occultation type is passed.
    """

    if occultation_type == 'transit':
        # Format the out-of-transit integration numbers.
        out_frames = np.abs(out_frames)
        out_frames = np.concatenate([np.arange(out_frames[0]),
                                     np.arange(out_frames[1]) - out_frames[1]])
    elif occultation_type == 'eclipse' or occultation_type == 'phase_curve':
        # Format the in-eclpse integration numbers.
        out_frames = np.linspace(out_frames[0], out_frames[1],
                                 out_frames[1] - out_frames[0] + 1).astype(int)
    else:
        msg = 'Unknown Occultaton Type: {}'.format(occultation_type)
        raise ValueError(msg)

    return out_frames

def open_filetype(datafile):
    """Open a datamodel whether it is a path, or the datamodel itself.

    Parameters
    ----------
    datafile : str, jwst.datamodel
        Datamodel or path to datamodel.

    Returns
    -------
    data : jwst.datamodel
        Opened datamodel.

    Raises
    ------
    ValueError
        If the filetype passed is not str or jwst.datamodel.
    """

    if isinstance(datafile, str):
        data = datamodels.open(datafile)
    elif isinstance(datafile, (datamodels.CubeModel, datamodels.RampModel,
                               datamodels.MultiSpecModel)):
        data = datafile
    else:
        raise ValueError('Invalid filetype: {}'.format(type(datafile)))

    return data

def make_deepstack(cube):
    """Make deep stack of a TSO.

    Parameters
    ----------
    cube : array-like[float]
        Stack of all integrations in a TSO

    Returns
    -------
    deepstack : array-like[float]
       Median of the input cube along the integration axis.
    """

    # Take median of input cube along the integration axis.
    deepstack = bn.nanmedian(cube, axis=0)

    return deepstack
