#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Frquently used functions shared by multiple steps

"""

from jwst import datamodels
import bottleneck as bn
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import chebyshev
import os


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

def poly_tracefind(data_copy, max_order=30, output_dir=None, save_figs=False,
                   show_figs=False, debug=False):
    """
    Function to find the spectrum trace using spline.
    Args:
        data_copy: array, copy of input data array with reference pixels removed
        max_order: integer, maximum order to attempt
        output_dir: string or None, path where to place outputs. Default is same dir as input file
        save_figs: boolean, default is False
        show_figs: boolean, if True only the 0th and nintegrations/2 th plots will be show
        debug: boolean
    Author:
        Maria Pena-Guerrero (pena@stsci.edu)
    Returns:
        trace_x: list of nintegrations arrays, x-location of the trace
        trace_y: list of nintegrations arrays, y-location of the trace
    """
    if debug:
        save_figs = False
        show_figs = True

    # loop through the integrations to create the whitelight curve
    nintegrations, rows, cols = np.shape(data_copy)
    trace_x, trace_y = [], []
    for i in range(nintegrations):
        # gather all the maximum flux values per column
        max_flx_list, trace_xi_idx, trace_yi_idx = [], np.array([]), np.array([])
        for xi in range(cols):
            flx = data_copy[i, :, xi]
            max_flx_list.append(max(flx))
            y_max = np.where(flx == max(flx))[0]
            print(y_max)
            trace_xi_idx = np.append(trace_xi_idx, xi)
            trace_yi_idx = np.append(trace_yi_idx, y_max)

        # Try orders from 1 to max in the polynomial for all the traces:
        orders = select_cheby_order(trace_xi_idx, trace_yi_idx, 1, max_order)

        # Select best order:
        order = int(np.median(orders))
        if debug:
            print('Best polynomial order was: ', order)

        # Use the best-one as deemed by the BIC to fit the trace
        print(i, len(trace_xi_idx), len(trace_yi_idx))
        coefficients = chebyshev.chebfit(trace_xi_idx, trace_yi_idx, deg=order)
        y_smooth_idx = chebyshev.chebval(trace_xi_idx, coefficients)
        trace_x.append(trace_xi_idx)
        trace_y.append(y_smooth_idx)

        # plot
        if save_figs or show_figs:
            if i == 0 or i == int(nintegrations/2.0):
                # make sanity-check plot
                plt.figure(figsize=(12, 4))
                im = plt.imshow(data_copy[i])
                plt.gca().invert_yaxis()  # so that axis has 0 at bottom left
                # add to sanity-check plot
                plt.plot(trace_x[i], trace_y[i], color='red', lw=1, alpha=0.5)
                plt.colorbar()
                plt.title("Trace find using polynomial function \n")
                if output_dir is None:
                    output_dir = ""
                plt.savefig(os.path.join(output_dir, "polytrace_i"+repr(i)+".png"))
                if show_figs:
                    plt.show()
                plt.close()

        if debug:
            # break after the 2nd integration
            if i == 2:
                break

    return trace_x, trace_y

def select_cheby_order(x, y, min_order, max_order):
    """
    This function selects (and returns) the optimal order of a Chebyshev polynomial using the BIC.

    Author:
        Doug Long (dlong@stsci.edu)

    Parameters
    ----------
    x: ndarray
        Array with the regressors
    y: ndarray
        Array with the data
    min_order: int
        Minimum order to try
    max_order: int
        Maximum order to try
    """
    orders = np.arange(min_order, max_order)
    bics = np.zeros(len(orders))

    # Fit only non-nans:
    idx = np.where(~np.isnan(y))[0] - 1
    n = len(idx)

    for i in range(len(orders)):
        order = orders[i]
        coeffs = chebyshev.chebfit(x[idx-1], y[idx], deg=order)
        RSS = np.sum((y - chebyshev.chebval(x[idx], coeffs))**2)
        bics[i] = n * np.log(RSS / n) + (order + 1) * np.log(n)
    idx = np.where(np.min(bics) == bics)[0]
    return orders[idx][0]
