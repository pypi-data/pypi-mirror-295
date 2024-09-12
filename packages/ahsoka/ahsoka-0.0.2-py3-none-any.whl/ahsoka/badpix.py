#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bad pixel correction from supreme-SPOON by Michael Radica

Made self-contained for use in ahsoka

"""

from astropy.io import fits
import glob
import numpy as np
from tqdm import tqdm
from scipy.ndimage import median_filter
import warnings
import bottleneck as bn

from jwst import datamodels

class BadPixStep:
    """Wrapper around custom Bad Pixel Correction Step.
    """

    def __init__(self, input_data, smoothed_wlc, baseline_ints,
                 output_dir='./', occultation_type='transit', filter='CLEAR'):
        """Step initializer.
        """

        self.tag = 'badpixstep.fits'
        self.output_dir = output_dir
        self.smoothed_wlc = smoothed_wlc
        self.baseline_ints = baseline_ints
        self.occultation_type = occultation_type
        self.filter = filter
        self.datafiles = np.atleast_1d(input_data)
        self.fileroots = get_filename_root(self.datafiles)
        self.fileroot_noseg = get_filename_root_noseg(self.fileroots)

    def run(self, thresh=10, box_size=5, max_iter=1, save_results=True,
            force_redo=False):
        """Method to run the step.
        """

        all_files = glob.glob(self.output_dir + '*')
        do_step = 1
        results = []
        for i in range(len(self.datafiles)):
            # If an output file for this segment already exists, skip the step.
            expected_file = self.output_dir + self.fileroots[i] + self.tag
            expected_deep = self.output_dir + self.fileroot_noseg + 'deepframe.fits'
            if expected_file not in all_files or expected_deep not in all_files:
                do_step = 0
                break
            else:
                results.append(datamodels.open(expected_file))
                deepframe = fits.getdata(expected_deep)
        if do_step == 1 and force_redo is False:
            print('Output files already exist.')
            print('Skipping Bad Pixel Correction Step.\n')
        # If no output files are detected, run the step.
        else:
            step_results = badpixstep(self.datafiles,
                                      baseline_ints=self.baseline_ints,
                                      smoothed_wlc=self.smoothed_wlc,
                                      output_dir=self.output_dir,
                                      save_results=save_results,
                                      fileroots=self.fileroots,
                                      fileroot_noseg=self.fileroot_noseg,
                                      occultation_type=self.occultation_type,
                                      filter=self.filter,
                                      max_iter=max_iter, thresh=thresh,
                                      box_size=box_size)
            results, deepframe = step_results

        return results, deepframe
    
def badpixstep(datafiles, baseline_ints, smoothed_wlc=None, thresh=10,
               box_size=5, max_iter=1, output_dir='./', save_results=True,
               fileroots=None, fileroot_noseg='', occultation_type='transit', filter='CLEAR'):
    """Identify and correct hot pixels remaining in the dataset. Find outlier
    pixels in the median stack and correct them via the median of a box of
    surrounding pixels. Then replace these pixels in each integration via the
    wlc scaled median.

    Parameters
    ----------
    datafiles : array-like[str], array-like[RampModel]
        List of paths to datafiles for each segment, or the datamodels
        themselves.
    baseline_ints : array-like[int]
        Integrations of ingress and egress.
    smoothed_wlc : array-like[float]
        Estimate of the normalized light curve.
    thresh : int
        Sigma threshold for a deviant pixel to be flagged.
    box_size : int
        Size of box around each pixel to test for deviations.
    max_iter : int
        Maximum number of outlier flagging iterations.
    output_dir : str
        Directory to which to output results.
    save_results : bool
        If True, save results to file.
    fileroots : array-like[str], None
        Root names for output files.
    fileroot_noseg : str
        Root file name with no segment information.
    occultation_type : str
        Type of occultation, either 'transit' or 'eclipse'.

    Returns
    -------
    data : list[CubeModel]
        Input datamodels for each segment, corrected for outlier pixels.
    deepframe : array-like[float]
        Final median stack of all outlier corrected integrations.
    """

    print('Starting custom hot pixel interpolation step.')

    # Output directory formatting.
    if output_dir is not None:
        if output_dir[-1] != '/':
            output_dir += '/'

    datafiles = np.atleast_1d(datafiles)
    # Format the baseline frames - either out-of-transit or in-eclipse.
    baseline_ints = format_out_frames(baseline_ints,
                                            occultation_type)

    data = []
    # Load in datamodels from all segments.
    for i, file in enumerate(datafiles):
        currentfile = open_filetype(file)
        data.append(currentfile)

        # To create the deepstack, join all segments together.
        # Also stack all the dq arrays from each segement.
        if i == 0:
            cube = currentfile.data
            dq_cube = currentfile.dq
        else:
            cube = np.concatenate([cube, currentfile.data], axis=0)
            dq_cube = np.concatenate([dq_cube, currentfile.dq], axis=0)

    # Initialize starting loop variables.
    newdata = np.copy(cube)
    newdq = np.copy(dq_cube)
    it = 0

    while it < max_iter:
        print('Starting iteration {0} of {1}.'.format(it + 1, max_iter))

        # Generate the deepstack.
        print(' Generating a deep stack...')
        deepframe = make_deepstack(newdata[baseline_ints])
        badpix = np.zeros_like(deepframe)
        count = 0
        nint, dimy, dimx = np.shape(newdata)

        # Loop over whole deepstack and flag deviant pixels.
        for i in tqdm(range(4, dimx-4)):
            for j in range(dimy):
                box_size_i = box_size
                box_prop = get_interp_box(deepframe, box_size_i, i, j,
                                                dimx)
                # Ensure that the median and std dev extracted are good.
                # If not, increase the box size until they are.
                while np.any(np.isnan(box_prop)):
                    box_size_i += 1
                    box_prop = get_interp_box(deepframe, box_size_i, i,
                                                    j, dimx)
                med, std = box_prop[0], box_prop[1]

                # If central pixel is too deviant (or nan/negative) flag it.
                if np.abs(deepframe[j, i] - med) >= (thresh * std) or np.isnan(deepframe[j, i]) or deepframe[j, i] < 0:
                    mini, maxi = np.max([0, i - 1]), np.min([dimx - 1, i + 1])
                    minj, maxj = np.max([0, j - 1]), np.min([dimy - 1, j + 1])
                    badpix[j, i] = 1
                    # Also flag cross around the central pixel.
                    badpix[maxj, i] = 1
                    badpix[minj, i] = 1
                    badpix[j, maxi] = 1
                    badpix[j, mini] = 1
                    count += 1

        print(' {} bad pixels identified this iteration.'.format(count))
        # End if no bad pixels are found.
        if count == 0:
            break
        # Replace the flagged pixels in the median integration.
        newdeep, deepdq =do_replacement(deepframe, badpix,
                                               dq=np.ones_like(deepframe),
                                               box_size=box_size)

        # If no lightcurve is provided, estimate it from the current data.
        if smoothed_wlc is None:
            if currentfile.meta.exposure.type == 'NIS_SOSS':
                postage = cube[:, 20:60, 1500:1550] #SOSS
            if currentfile.meta.exposure.type == 'NRS_BRIGHTOBJ':
                postage = cube[:, 6:25, 15:483] #PRISM
            timeseries = np.nansum(postage, axis=(1, 2))
            timeseries = timeseries / np.nanmedian(timeseries[baseline_ints])
            if filter == 'CLEAR':
                # Smooth the time series on a timescale of roughly 2%.
                smoothed_wlc = median_filter(timeseries,
                                         int(0.02*np.shape(cube)[0]))
            else:
                smoothed_wlc = timeseries / timeseries
        # Replace hot pixels in each integration using a scaled median.
        newdeep = np.repeat(newdeep, nint).reshape(dimy, dimx, nint)
        newdeep = newdeep.transpose(2, 0, 1) * smoothed_wlc[:, None, None]
        mask = badpix.astype(bool)
        newdata[:, mask] = newdeep[:, mask]
        # Set DQ flags for these pixels to zero (use the pixel).
        deepdq = ~deepdq.astype(bool)
        newdq[:, deepdq] = 0

        it += 1
        thresh += 1

    # Generate a final corrected deep frame for the baseline integrations.
    deepframe = make_deepstack(newdata[baseline_ints])

    current_int = 0
    # Save interpolated data.
    for n, file in enumerate(data):
        currentdata = file.data
        nints = np.shape(currentdata)[0]
        file.data = newdata[current_int:(current_int + nints)]
        file.dq = newdq[current_int:(current_int + nints)]
        current_int += nints
        if save_results is True:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                file.write(output_dir + fileroots[n] + 'badpixstep.fits')
        file.close()

    if save_results is True:
        # Save deep frame.
        hdu = fits.PrimaryHDU(deepframe)
        hdu.writeto(output_dir + fileroot_noseg + 'deepframe.fits',
                    overwrite=True)

    return data, deepframe

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


def get_filename_root_noseg(fileroots):
    """Get the file name root for a SOSS TSO woth noo segment information.

    Parameters
    ----------
    fileroots : array-like[str]
        File root names for each segment.

    Returns
    -------
    fileroot_noseg : str
        File name root with no segment information.
    """

    # Get total file root, with no segment info.
    working_name = fileroots[0]
    if 'seg' in working_name:
        parts = working_name.split('seg')
        part1, part2 = parts[0][:-1], parts[1][3:]
        fileroot_noseg = part1 + part2
    else:
        fileroot_noseg = fileroots[0]

    return fileroot_noseg

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
                               datamodels.MultiSpecModel, datamodels.SlitModel)):
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

def get_interp_box(data, box_size, i, j, dimx):
    """Get median and standard deviation of a box centered on a specified
    pixel.

    Parameters
    ----------
    data : array-like[float]
        Data frame.
    box_size : int
        Size of box to consider.
    i : int
        X pixel.
    j : int
        Y pixel.
    dimx : int
        Size of x dimension.

    Returns
    -------
    box_properties : array-like
        Median and standard deviation of pixels in the box.
    """

    # Get the box limits.
    low_x = np.max([i - box_size, 0])
    up_x = np.min([i + box_size, dimx - 1])

    # Calculate median and std deviation of box - excluding central pixel.
    box = np.concatenate([data[j, low_x:i], data[j, (i+1):up_x]])
    median = np.nanmedian(box)
    stddev = np.sqrt(outlier_resistant_variance(box))

    # Pack into array.
    box_properties = np.array([median, stddev])

    return box_properties

def do_replacement(frame, badpix_map, dq=None, box_size=5):
    """Replace flagged pixels with the median of a surrounding box.

    Parameters
    ----------
    frame : array-like[float]
        Data frame.
    badpix_map : array-like[bool]
        Map of pixels to be replaced.
    dq : array-like[int]
        Data quality flags.
    box_size : int
        Size of box to consider.

    Returns
    -------
    frame_out : array-like[float]
        Input frame wth pixels interpolated.
    dq_out : array-like[int]
        Input dq map with interpolated pixels set to zero.
    """

    dimy, dimx = np.shape(frame)
    frame_out = np.copy(frame)
    # Get the data quality flags.
    if dq is not None:
        dq_out = np.copy(dq)
    else:
        dq_out = np.zeros_like(frame)

    # Loop over all flagged pixels.
    for i in range(dimx):
        for j in range(dimy):
            if badpix_map[j, i] == 0:
                continue
            # If pixel is flagged, replace it with the box median.
            else:
                med = get_interp_box(frame, box_size, i, j, dimx)[0]
                frame_out[j, i] = med
                # Set dq flag of inerpolated pixel to zero (use the pixel).
                dq_out[j, i] = 0

    return frame_out, dq_out

def outlier_resistant_variance(data):
    """Calculate the varaince of some data along the 0th axis in an outlier
    resistant manner.
    """

    var = (bn.nanmedian(np.abs(data - bn.nanmedian(data, axis=0)), axis=0) / 0.6745)**2
    return var