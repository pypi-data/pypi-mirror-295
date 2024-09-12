#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
useful things from supreme-SPOON by Michael Radica

"""
import os
import numpy as np

from jwst import datamodels


def fix_filenames(old_files, to_remove, outdir, to_add=''):
    """Hacky function to remove file extensions that get added when running a
    default JWST DMS step after a custom one.

    Parameters
    ----------
    old_files : array-like[str], array-like[jwst.datamodel]
        List of datamodels or paths to datamodels.
    to_remove : str
        File name extension to be removed.
    outdir : str
        Directory to which to save results.
    to_add : str
        Extention to add to the file name.

    Returns
    -------
    new_files : array-like[str]
        New file names.
    """

    old_files = np.atleast_1d(old_files)
    new_files = []
    # Open datamodel and get file name.
    for file in old_files:
        if isinstance(file, str):
            file = datamodels.open(file)
        old_filename = file.meta.filename

        # Remove the unwanted extention.
        split = old_filename.split(to_remove)
        new_filename = split[0] + '_' + split[1]
        # Add extension if necessary.
        if to_add != '':
            temp = new_filename.split('.fits')
            new_filename = temp[0] + '_' + to_add + '.fits'

        # Save file with new filename
        file.write(outdir + new_filename)
        new_files.append(outdir + new_filename)
        file.close()

        # Get rid of old file.
        os.remove(outdir + old_filename)

    return new_files
