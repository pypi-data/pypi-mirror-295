#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
background correction from supreme-SPOON by Michael Radica

Made self-contained for use in ahsoka

"""

from astropy.io import fits
import bottleneck as bn
import glob
import numpy as np
import warnings


from jwst import datamodels

class SossClearBackgroundStep:
    """Wrapper around custom Background Subtraction step.
    """

    def __init__(self, input_data, background_model, output_dir='./'):
        """Step initializer.
        """

        self.tag = 'backgroundstep.fits'
        self.background_model = background_model
        self.output_dir = output_dir
        self.datafiles = np.atleast_1d(input_data)
        self.fileroots = get_filename_root(self.datafiles)
        self.fileroot_noseg = get_filename_root_noseg(self.fileroots)

    def run(self, save_results=True, force_redo=False, **kwargs):
        """Method to run the step.
        """

        all_files = glob.glob(self.output_dir + '*')
        do_step = 1
        results, background_models = [], []
        for i in range(len(self.datafiles)):
            # If an output file for this segment already exists, skip the step.
            expected_file = self.output_dir + self.fileroots[i] + self.tag
            expected_bkg = self.output_dir + self.fileroot_noseg + 'background.npy'
            if expected_file not in all_files or expected_bkg not in all_files:
                do_step = 0
                break
            else:
                results.append(datamodels.open(expected_file))
                background_models.append(np.load(expected_bkg))
        if do_step == 1 and force_redo is False:
            print('Output files already exist.')
            print('Skipping Background Subtraction Step.')
        # If no output files are detected, run the step.
        else:
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')
                scale1, scale2 = None, None
                if 'scale1' in kwargs.keys():
                    scale1 = kwargs['scale1']
                if 'scale2' in kwargs.keys():
                    scale2 = kwargs['scale2']
                step_results = sossclearbackgroundstep(self.datafiles,
                                              self.background_model,
                                              output_dir=self.output_dir,
                                              save_results=save_results,
                                              fileroots=self.fileroots,
                                              fileroot_noseg=self.fileroot_noseg,
                                              scale1=scale1, scale2=scale2)
                results, background_models = step_results

        return results, background_models
    
def sossclearbackgroundstep(datafiles, background_model, output_dir='./',
                   save_results=True, fileroots=None, fileroot_noseg='',
                   scale1=None, scale2=None):
    """Background subtraction must be carefully treated with SOSS observations.
    Due to the extent of the PSF wings, there are very few, if any,
    non-illuminated pixels to serve as a sky region. Furthermore, the zodi
    background has a unique stepped shape, which would render a constant
    background subtraction ill-advised. Therefore, a background subtracton is
    performed by scaling a model background to the countns level of a median
    stack of the exposure. This scaled model background is then subtracted
    from each integration.

    Parameters
    ----------
    datafiles : array-like[str], array-like[CubeModel]
        Paths to data segments for a SOSS exposure, or the datamodels
        themselves.
    background_model : array-like[float]
        Background model. Should be 2D (dimy, dimx)
    output_dir : str
        Directory to which to save outputs.
    save_results : bool
        If True, save outputs to file.
    fileroots : array-like[str]
        Root names for output files.
    fileroot_noseg : str
        Root name with no segment information.
    scale1 : float, None
        Scaling value to apply to background model to match data. Will take
        precedence over calculated scaling value. If only scale1 is provided,
        this will multiply the entire frame. If scale2 is also provided, this
        will be the "pre-stp" scaling.
    scale2 : float, None
        "Post-step" scaling value. scale1 must also be passed if this
        parameter is not None.


    Returns
    -------
    results : array-like[CubeModel]
        Input data segments, corrected for the background.
    model_scaled : array-like[float]
        Background model, scaled to the flux level of each group median.
    """

    print('Starting background subtraction step.')
    # Output directory formatting.
    if output_dir is not None:
        if output_dir[-1] != '/':
            output_dir += '/'

    datafiles = np.atleast_1d(datafiles)
    opened_datafiles = []
    # Load in each of the datafiles.
    for i, file in enumerate(datafiles):
        currentfile = open_filetype(file)
        opened_datafiles.append(currentfile)
        # To create the deepstack, join all segments together.
        if i == 0:
            cube = currentfile.data
        else:
            cube = np.concatenate([cube, currentfile.data], axis=0)
    datafiles = opened_datafiles

    # Make median stack of all integrations to use for background scaling.
    # This is to limit the influence of cosmic rays, which can greatly effect
    # the background scaling factor calculated for an individual inegration.
    print('Generating a deep stack using all integrations.')
    deepstack = make_deepstack(cube)
    # If applied at the integration level, reshape deepstack to 3D.
    if np.ndim(deepstack) != 3:
        dimy, dimx = np.shape(deepstack)
        deepstack = deepstack.reshape(1, dimy, dimx)
    ngroup, dimy, dimx = np.shape(deepstack)

    print('Calculating background model scaling.')
    model_scaled = np.zeros_like(deepstack)
    if scale1 is None:
        print(' Scale factor(s):')
    else:
        print(' Using user-defined background scaling(s):')
        if scale2 is not None:
            print('  Pre-step scale factor: {:.5f}'.format(scale1))
            print('  Post-step scale factor: {:.5f}'.format(scale2))
        else:
            print('  Background scale factor: {:.5f}'.format(scale1))
    first_time = True
    for i in range(ngroup):
        if scale1 is None:
            # Calculate the scaling of the model background to the median
            # stack.
            if dimy == 96:
                # Use area in bottom left corner of detector for SUBSTRIP96.
                xl, xu = 5, 21
                yl, yu = 5, 401
            else:
                # Use area in the top left corner of detector for SUBSTRIP256
                xl, xu = 210, 250
                yl, yu = 250, 500
            bkg_ratio = deepstack[i, xl:xu, yl:yu] / background_model[xl:xu, yl:yu]
            # Instead of a straight median, use the median of the 2nd quartile
            # to limit the effect of any remaining illuminated pixels.
            q1 = np.nanpercentile(bkg_ratio, 25)
            q2 = np.nanpercentile(bkg_ratio, 50)
            ii = np.where((bkg_ratio > q1) & (bkg_ratio < q2))
            scale_factor = np.nanmedian(bkg_ratio[ii])
            if scale_factor < 0:
                scale_factor = 0
            print('  Background scale factor: {1:.5f}'.format(i + 1, scale_factor))
            model_scaled[i] = background_model * scale_factor
        elif scale1 is not None and scale2 is None:
            # If using a user specified scaling for the whole frame.
            model_scaled[i] = background_model * scale1
        else:
            # If using seperate pre- and post- step scalings.
            # Locate the step position using the gradient of the background.
            grad_bkg = np.gradient(background_model, axis=1)
            step_pos = np.argmax(grad_bkg[:, 10:-10], axis=1)
            # Seperately scale both sides of the step.
            for j in range(dimy):
                model_scaled[i, j, :(step_pos[j]+8)] = background_model[j, :(step_pos[j]+8)] * scale1
                model_scaled[i, j, (step_pos[j]+8):] = background_model[j, (step_pos[j]+8):] * scale2

    # Loop over all segments in the exposure and subtract the background from
    # each of them.
    results = []
    for i, currentfile in enumerate(datafiles):
        # Subtract the scaled background model.
        data_backsub = currentfile.data - model_scaled
        currentfile.data = data_backsub

        # Save the results to file if requested.
        if save_results is True:
            if first_time is True:
                # Scaled model background.
                np.save(output_dir + fileroot_noseg + 'background.npy',
                        model_scaled)
                first_time = False
            # Background subtracted data.
            currentfile.write(output_dir + fileroots[i] + 'backgroundstep.fits')

        results.append(currentfile)
        currentfile.close()

    return results, model_scaled

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
