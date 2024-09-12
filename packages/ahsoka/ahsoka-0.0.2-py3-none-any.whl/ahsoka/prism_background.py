#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
background correction for prism data

Adapted from rm_background.py by Maria A. Pena-Guerrero

"""

from astropy.io import fits
import numpy as np
import glob
import warnings

from jwst import datamodels

from ahsoka.utils import get_filename_root, get_filename_root_noseg, poly_tracefind, open_filetype

class PrismBackgroundStep:
    """Wrapper around custom background subtraction step
    """

    def __init__(self, input_data, output_dir='./', save_figs=True, show_figs=False, debug=False):
        """Step initializer.
        """

        self.tag = 'backgroundstep.fits'
        self.output_dir = output_dir
        self.datafiles = np.atleast_1d(input_data)
        self.fileroots = get_filename_root(self.datafiles)
        self.fileroot_noseg = get_filename_root_noseg(self.fileroots)
        self.save_figs = save_figs
        self.show_figs = show_figs
        self.debug = debug 

    def run(self, save_results=True, force_redo=False, **kwargs):
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
            print('Skipping Background Subtraction Step.')
        # If no output files are detected, run the step.
        else:
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')
                step_results = prismbackgroundstep(self.datafiles,output_dir=self.output_dir, save_figs=self.save_figs, show_figs=self.show_figs, debug=self.debug)
                results = step_results

        return results
    
def prismbackgroundstep(datafiles, output_dir='./', save_figs=True, show_figs=False, debug=False):
    
    print('Starting background subtraction step.')
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

    print('\nUsing polynomial to find traces... \n')
    trace_x, trace_y = poly_tracefind(cube, max_order=30, output_dir=output_dir,
                                    save_figs=save_figs, show_figs=show_figs, debug=debug)
    
    
