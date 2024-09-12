#!/usr/bin/python3

import os
import time
import json
import numpy as np
from astropy.io import fits
from copy import deepcopy
from matplotlib import pyplot as plt
from scipy import ndimage
from scipy import stats
from scipy.interpolate import splrep, splev
from numpy.polynomial import chebyshev


"""
This script is to do a sanity check on the data by creating a white light curve
for the given data.

Authors
    Many people involved. Script created by Maria Pena-Guerrero (pena@stsci.edu),
    though each function has its corresponding author.

Usage

- As a module:
  import rm_background
  data_path = '/somewhere_data_lives/blah.fits'
  output_dir = '/somewhere'   # default is same place as input data
  spectrum_width = 12
  tracefind = None  # other allowed values: 'poly', 'spline', 'nonparam'
  background_function = None  # other allowed values: 'hst', 'webb'
  band_height = 'all'  # other allowed values: integers
  save_figs, show_figs, debug = True, False, False
  rm_background.rm_background(data_path, output_dir=output_dir, spectrum_width=spectrum_width,
                              tracefind=tracefind, background_function=background_function,
                              band_height=band_height, save_figs=save_figs,
                              show_figs=show_figs, debug=debug)

"""

__version__ = "1.0"

# HISTORY
# Nov 2021 - Version 1.0: initial version completed


def get_mad_sigma(x):
    """
    Author:
        Nestor Espinoza (nespinoza@stsci.edu)
    """
    x_median = np.nanmedian(x)
    return 1.4826 * np.nanmedian( np.abs(x - x_median) )


def trace_spectrum(image, dqflags, xstart, ystart, profile_radius=20, nsigma=100, gauss_filter_width=10,
                   xend=None, y_tolerance=5, verbose=False, instrument='niriss'):
    """
    Function that non-parametrically traces NIRISS/SOSS spectra. First, to get the centroid at xstart and
    ystart, it convolves the spatial profile with a gaussian filter, finding its peak through usual flux-weighted
    centroiding. Next, this centroid is used as a starting point to find the centroid of the left column through
    the same algorithm.

    Author:
        Nestor Espinoza (nespinoza@stsci.edu)

    Args:
        image: numpy.array
           The image that wants to be traced.
        dqflags: ndarray
           The data quality flags for each pixel in the image. Only pixels with DQ flags of zero will be used
           in the centroiding.
        xstart: float
           The x-position (column) on which the tracing algorithm will be started
        ystart: float
           The estimated y-position (row) of the center of the trace. An estimate within 10-20 pixels is enough.
        profile_radius: float
           Expected radius of the profile measured from its center. Only this region will be used to estimate
           the centroids of the spectrum.
        nsigma : float
           Median filters are applied to each column in search of outliers. This number defines how many
           n-sigma above the noise level the residuals of the median filter and the image should be
           considered outliers.
        gauss_filter_width: float
           Width of the gaussian filter used to perform the centroiding of the first column
        xend: int
           x-position at which tracing ends. If none, trace all the columns left to xstart.
        y_tolerance: float
           When tracing, if the difference between the two difference centroids at two contiguous columns
           is larger than this, then assume tracing failed (e.g., cosmic ray).
        verbose: boolean
           If True, print error messages.
        instrument: string
           Name of the instument used - This was added by M. Pena-Guerrero for NIRSpec data

    Returns:
        x: numpy.array
           Columns at which the centroid is calculated.
        y: numpy.array
           Calculated centroids.
    """

    # Define x-axis:
    if xend is not None:
       x = np.arange(xend, xstart + 1)
    else:
       x = np.arange(0, xstart + 1)

    # Define y-axis:
    y = np.arange(image.shape[0])

    # Define status of good/bad for each centroid:
    status = np.full(len(x), True, dtype=bool)

    # Define array that will save centroids at each x:
    ycentroids = np.zeros(len(x))

    for i in range(len(x))[::-1]:
        xcurrent = x[i]

        # Perform median filter to identify nasty (i.e., cosmic rays) outliers in the column:
        mf = ndimage.median_filter(image[:,xcurrent], size=5)
        residuals = mf - image[:,xcurrent]
        mad_sigma = get_mad_sigma(residuals)
        column_nsigma = np.abs(residuals) / mad_sigma

        # Extract data-quality flags for current column; index good pixels --- mask nans as well:
        idx_good = np.where((dqflags[:, xcurrent] == 0) & (~np.isnan(image[:, xcurrent]) & (column_nsigma < nsigma)))[0]
        #idx_good = np.where ((~np.isnan(image[:, xcurrent]) & (column_nsigma < nsigma)))[0]
        #idx_good = np.where (~np.isnan(image[:,xcurrent]))[0]

        if (len(idx_good) > 0):
            # Convolve column with a gaussian filter; remove median before convolving:
            filtered_column = ndimage.gaussian_filter1d(image[idx_good,xcurrent] - \
                                               np.median(image[idx_good,xcurrent]), gauss_filter_width)

            # Find centroid within profile_radius pixels of the initial guess:
            idx = np.where(np.abs(y[idx_good]-ystart) < profile_radius)[0]
            ycentroids[i] = np.sum(y[idx_good][idx]*filtered_column[idx])/np.sum(filtered_column[idx])

            # Get the difference of the current centroid with the previous one (if any):
            if xcurrent != x[-1]:

                previous_centroid = ycentroids[i + 1]
                difference = np.abs(previous_centroid - ycentroids[i])

                if (difference > y_tolerance):

                   if verbose:
                       print('Tracing failed at column',xcurrent,'; estimated centroid:',ycentroids[i],', previous one:',previous_centroid,'> than tolerance: ',y_tolerance,\
                            '. Replacing with closest good trace position.')

                   ycentroids[i] = previous_centroid

                   # For NIRSpec, force the trace to be at the center of the aperture
                   if instrument == 'nirspec':
                       ycentroids[i] = np.shape(image)[0]/2.0

            ystart = ycentroids[i]
        else:
            #print(xcurrent,'is false')
            status[i] = False

    # Return only good centroids:
    idx_output = np.where(status)[0]
    return x[idx_output], ycentroids[idx_output]


def background(data, top_ap, low_ap, output_dir=None, save_figs=False, show_figs=False, debug=False):
    """
    Created Jan 2021
    Written by Lili Alderson (lili.alderson@bristol.ac.uk)
    Last updated: 2021/11/17

    Determines the background count via median of a suitable region extending across full width
    of image given the aperture being used around the spectral trace.

    Also plots a histogram of the counts in the background region

    Will initally attempt to create a background region the same width as the aperture/spectral
    trace and place the backgroud region either above or below the aperture/trace (whichever
    space is largest)
    However if the aperture/spectral trace fills the majority of the image, then the background
    region will be half the widith of the region above or below the aperture/trace (whichever is
    largest)

    Inputs:
    - data (array)
       fits file (or similar) in the form of an array. For HST/WFC3 data 5 pixel edge should
       already be removed
    - top_ap (int)
       the upper edge of the aperature being used for spectral trace extraction
    - low_ap (int)
       the lower edge of the aperature being used for spectral trace extraction
    - output_dir
        string or None, path where to place outputs. Default is same dir as input file
    - save_figs
        boolean, default is False
    - show_figs
        boolean, if True only the 0th and nintegrations/2 th plots will be show
    - debug
        boolean
    Outputs:
    - bck (float)
       the median of the background region
    - bck_array (array)
       an array equal in size to the original data input, to make background subraction easier
    - top_bck_edge (float)
       upper edge of the selected background region
    - low_bck_edge (float)
       lower edge of the selected background region
    - bkgd_masked (array)
        copy of input data array with masked out background (i.e. only object)
    """
    nrows, ncols = np.shape(data) # Get shape of image
    if abs(top_ap-low_ap) < nrows/2:
        if nrows - low_ap > top_ap:
            # nrows - (nrows-lop_ap)/2 gets you to half way between the edge of the image and the edge of the aperture
            # then taking or adding half the width of the aperture creates a new aperture centred around the midpoint of that section
            top_bck_edge = int(nrows - (nrows-low_ap)/2 - (low_ap - top_ap)/2)
            low_bck_edge = int(nrows - (nrows-low_ap)/2 + (low_ap - top_ap)/2)
        else:
            top_bck_edge = int(top_ap/2 - (low_ap-top_ap)/2)
            low_bck_edge = int(top_ap/2 + (low_ap-top_ap)/2)
    else: #for when the scan is too big to fit an aperture width above or below
        if debug:
            print("Scan too wide to use traditional method, background region will not be same width as aperture")
        if nrows - low_ap > top_ap:
            # nrows - (nrows-lop_ap)/2 gets you to half way between the edge of the image and the edge of the aperture
            # then taking or adding half the width of the aperture creates a new aperture centred around the midpoint of that section
            top_bck_edge = int(nrows - (nrows-low_ap)/2 - (nrows - low_ap)/4)
            low_bck_edge = int(nrows - (nrows-low_ap)/2 + (nrows - low_ap)/4)
        else:
            top_bck_edge = int(top_ap/2 - (top_ap)/4)
            low_bck_edge = int(top_ap/2 + (top_ap)/4)
        if debug:
            print("Background top_bck_edge, low_bck_edge: ", top_bck_edge, low_bck_edge)
            print("Background region has size: ", abs(top_bck_edge-low_bck_edge))
            #print(data[top_bck_edge:low_bck_edge, :])
    # remove nans, if any
    bck = np.median(data[top_bck_edge:low_bck_edge, :]).astype("float64")
    bck_array = np.full((nrows,ncols), bck)
    plt.figure()
    plt.hist(data[top_bck_edge:low_bck_edge,:].flatten(), 1000, density=True)
    #plt.xlim(0,700)
    plt.ylabel("Background Histogram Density")
    plt.xlabel("Counts")
    if debug:
        save_figs, show_figs = False, True
    if save_figs:
        if output_dir is None:
            output_dir = ""
        plt.savefig(os.path.join(output_dir, "background_histogram.png"))
    if show_figs:
        plt.show()
    plt.close()
    # create the array with the masked background - added by M. Pena-Guerrero
    bkgd_masked = deepcopy(data)
    bkgd_masked[0: top_bck_edge-1, :] = np.nan
    bkgd_masked[low_bck_edge+1: nrows, :] = np.nan
    return(bck, bck_array, top_bck_edge, low_bck_edge, bkgd_masked)


def background_wrapper(data, top_ap, low_ap, output_dir=None, save_figs=False, show_figs=False, debug=False):
    """
    Wrapper function for the background function created by Lili to work for all integrations and save the json file.
    Author:
        Maria Pena-Guerrero (pena@stsci.edu)
    Inputs:
    - data (array)
       fits file (or similar) in the form of an array. For HST/WFC3 data 5 pixel edge should
       already be removed
    - top_ap (int)
       the upper edge of the aperature being used for spectral trace extraction
    - low_ap (int)
       the lower edge of the aperature being used for spectral trace extraction
    - output_dir
        string or None, path where to place outputs. Default is same dir as input file
    - save_figs
        boolean, default is False
    - show_figs
        boolean, if True only the 0th and nintegrations/2 th plots will be show
    - debug
        boolean
    Outputs:
    - bkgd_value_dict (dictionary)
       dictionary of the median of the background region per integration
    - bck_array (array)
       an array equal in size to the original data input, to make background subraction easier
    - bkgd_masked (array)
        copy of input data array with masked out background (i.e. only object)
    """
    bkgd_value_dict, whole_bck_array, whole_bkgd_masked = {}, deepcopy(data), deepcopy(data)
    integrations, rows, cols = np.shape(data)
    for i in range(integrations):
        bck, bck_array, _, _, bkgd_masked = background(data[i], top_ap, low_ap, output_dir=output_dir,
                                                       save_figs=save_figs, show_figs=show_figs,
                                                       debug=debug)
        bkgd_value_dict[i] = bck
        whole_bck_array[i] = bck_array
        whole_bkgd_masked[i] = bkgd_masked
        if debug:
            # break after the 2nd integration
            if i == 2:
                break
    print('\n Dictionary of background values per integration: ', repr(bkgd_value_dict))
    return bkgd_value_dict, whole_bck_array, whole_bkgd_masked


def end_timer(start_time):
    """
    This function calculates the running time given a start time.
    Author:
        Maria Pena-Guerrero (pena@stsci.edu)
    Args:
        start_time: time object
    Returns:
        end_time: string
    """
    end_time = repr(time.time() - start_time)
    if (float(end_time)) > 60.0:
        end_time_min = float(end_time) / 60.  # this is in minutes
        if end_time_min > 60.0:
            end_time_hr = end_time_min / 60.  # this is in hours
            end_time = end_time + "sec = " + repr(round(end_time_hr, 1)) + "hr"
        else:
            end_time = end_time + "sec = " + repr(round(end_time_min, 1)) + "min"
    else:
        end_time = end_time + "sec"
    return end_time


def nonparam_tracefind(data_arr, dq_array, y_tolerance=5, instrument='nirspec',
                       output_dir=None, save_figs=False, show_figs=False, debug=False):
    """
    This is a wrapper function to call the non parametric trace function written by N. Espinoza
    Args:
        data_arr: array, pipeline TSO data i.e. 3 dimensions (integrations, rows, columns)
        dq_array: array, same dimensions as data_arr
        y_tolerance: integer, when tracing, if the difference between the two difference
                     centroids at two contiguous columns is larger than this,
                     then assume tracing failed (e.g., cosmic ray)
        instrument: string, name of instrument used
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

    # define needed quantities for tracing finding function
    nintegrations, rows, cols = np.shape(data_arr)
    xend, xstart = 0, cols-1
    yend, ystart = 0, rows-1

    # loop through the integrations
    trace_x, trace_y = [], []
    for i in range(nintegrations):
        trace_xi, trace_yi = trace_spectrum(data_arr[i], dq_array[i],
                                            xstart, ystart, xend=xend,
                                            y_tolerance=2,
                                            instrument='nirspec',
                                            verbose=False)
        trace_x.append(trace_xi)
        trace_y.append(trace_yi)

        if save_figs or show_figs:
            if i == 0 or i == int(nintegrations/2.0):
                # make sanity-check plot
                plt.figure(figsize=(12, 4))
                im = plt.imshow(data_arr[i])
                #im.set_clim(-3.0e-9,6.5e-8)
                plt.gca().invert_yaxis()  # so that axis has 0 at bottom left
                # add to sanity-check plot
                plt.plot(trace_x[i], trace_y[i], color='red', lw=1, alpha=0.5)
                plt.colorbar()
                plt.title("Trace find using non-parametric function \n")
                if output_dir is None:
                    output_dir = ""
                plt.savefig(os.path.join(output_dir, "nonpapramtrace_i"+repr(i)+".png"))
                if show_figs:
                    plt.show()
                plt.close()

        if debug:
            # break after the 2nd integration
            if i == 2:
                break
    return trace_x, trace_y


def rm_ref_pix(data_arr):
    """
    Function to remove reference pixels, if any
    Args:
        data_arr: array, pipeline TSO data i.e. 3 dimensions (integrations, rows, columns)
    Author:
        Maria Pena-Guerrero (pena@stsci.edu)
    Returns:
        data_copy: array, copy of input data array with reference pixels removed
        xstart: integer, index of where data in the x-axis starts in the frame of the input data array
        xend: integer, index of where data in the x-axis ends in the frame of the input data array
        ystart: integer, index of where data in the y-axis starts in the frame of the input data array
        yend: integer, index of where data in the y-axis ends in the frame of the input data array
    """
    # define needed quantities for tracing finding function
    nintegrations, rows, cols = np.shape(data_arr)
    xstart, xend = 0, cols
    ystart, yend = 0, rows
    # make sure not to include reference pixels
    if cols == 2048:
        xstart, xend = xstart+4, xend-4
    if rows == 2048:
        ystart, yend = ystart+4, yend-4
    data_copy = deepcopy(data_arr[:, ystart:yend, xstart:xend])
    return data_copy


def spline_tracefind(data_copy, n_interior_knots=5, output_dir=None, save_figs=False,
                     show_figs=False, debug=False):
    """
    Function to find the spectrum trace using spline.
    Args:
        data_copy: array, copy of input data array with reference pixels removed
        n_interior_knots: integer, number of knowts fot the spline
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

    print('\n* Spline using ', n_interior_knots, 'knots \n')

    nintegrations, rows, cols = np.shape(data_copy)
    trace_x, trace_y = [], []
    for i in range(nintegrations):
        # gather all the maximum flux values per column
        max_flx_list, trace_xi_idx, trace_yi_idx = [], np.array([]), np.array([])
        for xi in range(cols):
            flx = data_copy[i, :, xi]
            max_flx_list.append(max(flx))
            trace_xi_idx = np.append(trace_xi_idx, xi)  # append this index for trace at that column
            y_max = np.where(flx == max(flx))[0][0]
            trace_yi_idx = np.append(trace_yi_idx, y_max)

        # do the spline
        qs = np.linspace(0, 1, n_interior_knots+2)[1:-1]
        knots = np.quantile(trace_xi_idx, qs)
        xck = splrep(trace_xi_idx, trace_yi_idx, t=knots, k=3)
        y_smooth_idx = splev(trace_yi_idx, xck)
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
                plt.title("Trace find using spline function \n")
                if output_dir is None:
                    output_dir = ""
                plt.savefig(os.path.join(output_dir, "splinetrace_i"+repr(i)+".png"))
                if show_figs:
                    plt.show()
                plt.close()

        # if debugging stop after the first integration
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
            trace_xi_idx = np.append(trace_xi_idx, xi)
            trace_yi_idx = np.append(trace_yi_idx, y_max)

        # Try orders from 1 to max in the polynomial for all the traces:
        orders = select_cheby_order(trace_xi_idx, trace_yi_idx, 1, max_order)

        # Select best order:
        order = int(np.median(orders))
        if debug:
            print('Best polynomial order was: ', order)

        # Use the best-one as deemed by the BIC to fit the trace
        print("integration=",i,trace_xi_idx.shape, trace_yi_idx.shape)
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


def mask_spec(data_copy, trace_x, trace_y, spectrum_width=10, output_dir=None,
              save_figs=False, show_figs=False, debug=False):
    """
    This function masks out the spectrum either following the trace or with a user given rectangle.
    Args:
        data_copy: array, copy of input data array with reference pixels removed
        trace_x: list of nintegrations arrays, x-location of the trace
        trace_y: list of nintegrations arrays, y-location of the trace
        output_dir: string or None, path where to place outputs. Default is same dir as input file
        spectrum_width: integer, full width of spectrum in pixels
        show_figs: boolean, if True only the 0th and nintegrations/2 th plots will be show
        debug: boolean
    Author:
        Maria Pena-Guerrero (pena@stsci.edu)
    Returns:
        img_copy: array, copy of input data of same dimensions with spectrum trace masked out
                  (i.e. the spectrum area is set to NaN values)
        bkgd_masked: array, oposite of img_copy array, background is masked
    """
    if debug:
        save_figs = False
        show_figs = True

    nintegrations, rows, cols = np.shape(data_copy)
    img_copy = deepcopy(data_copy)
    bkgd_masked = deepcopy(data_copy)

    if spectrum_width is not None:
        spectrum_width = int(spectrum_width)
        spec_width_half = int(spectrum_width/2.0)

    for i in range(nintegrations):
        # get the trace flux indices - use round and add conditional to remain in the data limits
        trace_xi_idx = np.round(trace_x[i], 0).astype(int)
        trace_yi_idx = np.round(trace_y[i], 0).astype(int)
        for txi_idx, txi in enumerate(trace_xi_idx):
            if txi >= cols:
                trace_xi_idx[txi_idx] = cols - 1
            if txi < 0:
                trace_xi_idx[txi_idx] = 0
            if trace_yi_idx[txi_idx] >= rows:
                trace_yi_idx[txi_idx] = rows - 1
            if trace_yi_idx[txi_idx] < 0:
                trace_yi_idx[txi_idx] = 0
        # get the trace flux values
        flx_trace = []
        for j, tyi in enumerate(trace_yi_idx):
            f = data_copy[i, tyi, trace_xi_idx[j]]
            flx_trace.append(f)

        # check the fluxes where the fluxes are lower than the threshold
        trace_not_nan_xi, trace_not_nan_yi = [], []
        for xi in range(cols):
            flx = img_copy[i, :, xi]
            # define the flux threshold as 1% of the maximum positive flux value in the trace
            flx_threshold = max(flx) * 0.01
            # select the target flux indices
            if spectrum_width is None:
                target_flx_idx = np.where(flx > flx_threshold)
            else:
                # create the fixed-width 'box' that follows the trace
                for txi_idx, txi in enumerate(trace_xi_idx):
                    # set the limits for the trace
                    box_y = [trace_yi_idx[txi_idx] - spec_width_half, trace_yi_idx[txi_idx] + spec_width_half]
                    # set the trace box to nan
                    img_copy[i, box_y[0]: box_y[1]+1, 0: trace_xi_idx[txi_idx]] = np.nan
                    # set the background to nan
                    bkgd_masked[i, 0: box_y[0], 0: trace_xi_idx[txi_idx]] = np.nan
                    bkgd_masked[i, box_y[1]-1: rows, 0: trace_xi_idx[txi_idx]] = np.nan
                # exit the loop at this point
                continue

            # check if the trace +- 1 pixel is masked
            if xi in trace_xi_idx:
                trace_idx = list(trace_xi_idx).index(xi)
                tracexi = trace_xi_idx[trace_idx]
                traceyi = trace_yi_idx[trace_idx]
                if traceyi not in target_flx_idx[0]:
                    trace_not_nan_xi.append(tracexi)
                    trace_not_nan_yi.append(traceyi)
                if traceyi+1 not in target_flx_idx[0]:
                    trace_not_nan_xi.append(tracexi)
                    trace_not_nan_yi.append(traceyi+1)
                if traceyi-1 not in target_flx_idx[0]:
                    trace_not_nan_xi.append(tracexi)
                    trace_not_nan_yi.append(traceyi-1)

            # set flux values of the target trace to NaN in the image copy
            flx[target_flx_idx] = np.nan
            img_copy[i, :, xi] = flx
            # set the background to nan
            bgflx = bkgd_masked[i, :, xi]
            bgflx[~target_flx_idx] = np.nan
            bkgd_masked[i, :, xi] = bgflx

        # check if there are points along the trace that are not nan and do a box to mask if necessary
        if len(trace_not_nan_yi) > 0:
            left_xedge, right_xedge = [], []
            # check if there are too many crossings trhoughout the spectrum, if so use a default box
            xspec_mid_point = int(cols/2)
            # check which side is the crossing occuring
            for trace_cross in trace_not_nan_xi:
                if trace_cross < xspec_mid_point:
                    left_xedge.append(trace_cross)
                else:
                    right_xedge.append(trace_cross)

            # make y limits of box to mask out spectrum
            yspectrum_width = 10
            yspec_width_half = int(yspectrum_width/2.0)

            # create left edge 'box', i.e. set nans following the trace
            if len(left_xedge) > 0:
                # find limit for the left edge 'box'
                ledge = max(left_xedge)
                # create the index list of trace values to set to nans
                lefty = [*range(0, list(trace_xi_idx).index(ledge))]
                # check if the x-coord is repeated, and how many times
                max_reps = left_xedge.count(ledge)
                if max_reps > 1:
                    last_idx = lefty[-1]
                    for _ in range(max_reps):
                        lefty.append(last_idx+1)
                        last_idx += 1
                # loop through the trace values and set to nan
                for ly in lefty:
                    box_y = [trace_yi_idx[ly] - yspec_width_half, trace_yi_idx[ly] + yspec_width_half]
                    # set the trace crossings to nan
                    img_copy[i, box_y[0]: box_y[1]+1, 0: trace_xi_idx[ly]] = np.nan
                    # set the areas outside the 'box' to initial values below
                    img_copy[i, 0: box_y[0]-1, trace_xi_idx[ly]] = data_copy[i, 0: box_y[0]-1, trace_xi_idx[ly]]
                    bkgd_masked[i, 0: box_y[0]-1, trace_xi_idx[ly]] = data_copy[i, 0: box_y[0]-1, trace_xi_idx[ly]]
                    # set the areas outside the 'box' to initial values above
                    img_copy[i, box_y[1]+1: rows, trace_xi_idx[ly]] = data_copy[i, box_y[1]+1: rows, trace_xi_idx[ly]]
                    bkgd_masked[i, box_y[1]+1: rows, trace_xi_idx[ly]] = data_copy[i, box_y[1]+1: rows, trace_xi_idx[ly]]
                if debug:
                    print(' * Integration ', i, ' LEFT EDGE: Spectrum too weak, using default width to mask out pixels in x: 0 -',
                          ledge, ' and following the trace in y +-', yspec_width_half, ' pixels ')

            # create right edge box
            if len(right_xedge) > 0:
                # find the point at which to start the right 'box'
                redge = min(right_xedge)
                # create the index list of trace values to set to nans
                righty = [*range(list(trace_xi_idx).index(redge), len(trace_xi_idx))]
                # loop through the trace values and set to nan
                for ry in righty:
                    box_y = [trace_yi_idx[ry] - yspec_width_half, trace_yi_idx[ry] + yspec_width_half]
                    # set the trace crossings to nan
                    img_copy[i, box_y[0]: box_y[1]+1, trace_xi_idx[ry]] = np.nan
                    # set the areas outside the 'box' to initial values below
                    img_copy[i, 0: box_y[0]-1, trace_xi_idx[ry]] = data_copy[i, 0: box_y[0]-1, trace_xi_idx[ry]]
                    bkgd_masked[i, 0: box_y[0]-1, trace_xi_idx[ry]] = data_copy[i, 0: box_y[0]-1, trace_xi_idx[ry]]
                    # set the areas outside the 'box' to initial values above
                    img_copy[i, box_y[1]+1: rows, trace_xi_idx[ry]] = data_copy[i, box_y[1]+1: rows, trace_xi_idx[ry]]
                    bkgd_masked[i, box_y[1]+1: rows, trace_xi_idx[ry]] = data_copy[i, box_y[1]+1: rows, trace_xi_idx[ry]]
                if debug:
                    print(' * Integration ', i, ' RIGHT EDGE: Spectrum too weak, using default width to mask out pixels in x: ',
                          redge, '-', cols, ' and following the trace in y +-', yspec_width_half, ' pixels \n')

        if save_figs or show_figs:
            if i == 0 or i == int(nintegrations/2.0):
                # make sanity-check plot
                plt.figure(figsize=(10, 8))
                im = plt.imshow(img_copy[i])
                #im.set_clim(-3.0e-9,6.5e-8)
                plt.gca().invert_yaxis()  # so that axis has 0 at bottom left
                # add to sanity-check plot
                plt.plot(trace_x[i], trace_y[i], color='red', lw=1, alpha=0.5)
                plt.colorbar()
                plt.title("Background with masked out spectrum \n")
                if save_figs:
                    if output_dir is None:
                        output_dir = ""
                    plt.savefig(os.path.join(output_dir, "masked_spec_i"+repr(i)+".png"))
                if show_figs:
                    plt.show()
                plt.close()

        if debug:
            # break after the 2nd integration
            if i == 2:
                break
    return img_copy, bkgd_masked


def find_nearest_within(arr, value, threshold):
    '''
    This function gives the content in the array of the number that is closest to
    the value given, within threshold away from value.
    Args:
        arr: array to look into
        value: value to look for
        threshold: range of values to find the nearest value in the array
    Author:
        Maria Pena-Guerrero (pena@stsci.edu)
    Returns:
        the nearest value
    '''
    half_thres = threshold / 2.0
    choped_arr = arr[(arr >= value-half_thres) & (arr <= value+half_thres)]
    if len(choped_arr) == 0:
        return 0.0
    diff = np.abs(choped_arr - value)
    diff_min = min(diff)
    return np.squeeze(choped_arr[diff==diff_min])


def get_background(trace_x, trace_y, masked_data, height_from_spec=5, band_height=None,
                   output_dir=None, save_figs=False, show_figs=False, debug=False):
    """
    This function obtains a background value to be subtracted from the image, as well as the
    background array, via Local Background Estimation, using the following as guide for the
    algorithm: https://wise2.ipac.caltech.edu/docs/release/allsky/expsup/sec4_4c.html#back
    The idea is to use small bands instead of the circular annulus centered on the source.
    Author:
        Maria Pena-Guerrero (pena@stsci.edu)
    Agrs:
        trace_x: list of nintegrations arrays, x-location of the trace
        trace_y: list of nintegrations arrays, y-location of the trace
        masked_data: array, copy of input data array with spectrum trace masked out (i.e. the
                     spectrum area is set to NaN values and reference pixels are removed)
        height_from_spec: integer, number of pixels to go above and below to define the start
                          of the band
        band_height: integer, number of pixels that the define the height of the bands
              other allowed values:
                 None - background values will only be taken from a line parallel to the trace
                 'all' - the whole are above and below the initial background line will be used
        output_dir: string or None, path where to place outputs. Default is same dir as input file
        save_figs: boolean, default is False
        show_figs: boolean, if True only the 0th and nintegrations/2 th plots will be show
        debug: boolean
    Returns:
        bkgd_value: float, the median of the background region
        bck_array: array, an array equal in size to the original data input, to make
                   background subraction easier
    """
    nintegrations, rows, cols = np.shape(masked_data)

    bck_array = np.full((nintegrations, rows, cols), np.nan)
    bkgd_value_dict = {}

    # loop through the integrations
    for i in range(nintegrations):
        # go through the colums
        bkgd_valyidx_above, bkgd_valyidx_below = [], []
        bkgd_valxidx_above, bkgd_valxidx_below = [], []
        bkgd_values_above, bkgd_values_below = [], []
        bkgd_bandabove = np.full((rows, cols), np.nan)
        bkgd_bandbelow = np.full((rows, cols), np.nan)
        bkgd_bands, y_bkgd_vals, concat_bkgdvals = np.array([]), [], []
        for xi in range(cols):
            # get the flux slice according
            flx = masked_data[i, :, xi]
            # get all the NOT nan indexes
            nanidx_boolean = np.isnan(flx)
            not_nanidx = np.where(nanidx_boolean == False)[0]

            # find the point in the trace
            if xi in trace_x[i]:
                idx = list(trace_x[i]).index(xi)
                trace_x_i = trace_x[i][idx]
                trace_y_i = trace_y[i][idx]
            else:
                continue

            # define the band above the traced spectrum
            bkgd_yidx_above = int(trace_y_i) + height_from_spec
            skip_bkgd_yidx_above = False
            while True:
                if bkgd_yidx_above <= rows - 1:
                    # This value is within the image, now check that it is not a NaN
                    if bkgd_yidx_above in not_nanidx:
                        bkgd_valyidx_above.append(bkgd_yidx_above)
                        bkgd_valxidx_above.append(xi)
                        bkgd_values_above.append(flx[bkgd_yidx_above])
                        break
                    # try to find a value above the spectrum but below the top of the image
                    else:
                        # check if this is the highest possible value
                        if bkgd_yidx_above == rows - 1:
                            # there are no usable background values above the spectrum
                            # continue to the next column skipping this value
                            skip_bkgd_yidx_above = True
                            break
                        # go a bit further up and check again
                        bkgd_yidx_above += 1
                else:
                    # there are no usable background values above the spectrum
                    # end while skipping this value
                    skip_bkgd_yidx_above = True
                    break
            if skip_bkgd_yidx_above:
                continue

            # define the band below the spectrum
            bkgd_yidx_below = int(trace_y_i) - height_from_spec
            skip_bkgd_yidx_below = False
            while True:
                if bkgd_yidx_below >= 0:
                    # This value is within the image, now check that it is not a NaN
                    if bkgd_yidx_below in not_nanidx:
                        bkgd_valyidx_below.append(bkgd_yidx_below)
                        bkgd_valxidx_below.append(xi)
                        bkgd_values_below.append(flx[bkgd_yidx_below])
                        break
                    # try to find a value below the spectrum but above the bottom of the image
                    else:
                        # check if this is the highest possible value
                        if bkgd_yidx_above == 0:
                            # there are no usable background values below the spectrum
                            # continue to the next column skipping this value
                            skip_bkgd_yidx_below = True
                            break
                        # go a bit further up and check again
                        bkgd_yidx_below -= 1
                else:
                    # there are no usable background values below the spectrum
                    # end while skipping this value
                    skip_bkgd_yidx_below = True
                    break

            # now build the band
            if band_height is not None:
                # convert the input into an integer
                if isinstance(band_height, str):
                    if 'a' in band_height.lower():
                        band_height = int(rows - trace_y_i)
                    else:
                        band_height = int(band_height)
                # append all the band background values
                band_end = int(bkgd_yidx_above + band_height)
                if band_end >= rows:
                    band_end = rows
                band_start = int(bkgd_yidx_below - band_height)
                if band_start < 0:
                    band_start = 0
                bkgd_bands_xi = flx[band_start: band_end]
                bkgd_bands = np.append(bkgd_bands, bkgd_bands_xi)
                # make the arrays to plot
                flx_above = flx[bkgd_yidx_above: band_end]
                flx_below = flx[band_start: bkgd_yidx_below+1]
                bkgd_bandabove[bkgd_yidx_above: band_end, xi] = flx_above
                bkgd_bandbelow[band_start: bkgd_yidx_below+1, xi] = flx_below
                if debug:
                    # set the arrays to plot histograms
                    y_bkgd_vals_xi = [*range(band_start, bkgd_yidx_below+1)] + [*range(bkgd_yidx_above, band_end)]
                    y_bkgd_vals += list(y_bkgd_vals_xi)
                    concat_bkgdvals_xi = list(flx_below) + list(flx_above)
                    concat_bkgdvals = concat_bkgdvals + concat_bkgdvals_xi

                    # set to True if you want to see a few column histograms
                    do_col_hist = False

                    if do_col_hist:
                        if xi <= 1 or xi>14 and xi<18:
                            # do histogram per column
                            plt.figure(1, figsize=(10, 8))
                            plt.subplots_adjust(hspace=0.4)
                            alpha = 0.2
                            # top figure
                            # remove the NaN values to estimate the background value
                            nanidx_boolean_xi = np.isnan(bkgd_bands_xi)
                            notnanidx_xi = np.where(nanidx_boolean_xi == False)
                            if debug:
                                notnanidx_xi = notnanidx_xi[0]
                            notnan_bkgd_bands_xi = bkgd_bands_xi[notnanidx_xi]  # only keep the non-nan values
                            ax = plt.subplot(211)
                            n, bins, patches = ax.hist(notnan_bkgd_bands_xi, bins='auto', histtype='bar', ec='k', facecolor="blue", alpha=alpha)
                            x_mean = np.mean(notnan_bkgd_bands_xi)
                            x_median = np.median(notnan_bkgd_bands_xi)
                            #round_notnan_bkgd_bands_xi = np.round(notnan_bkgd_bands_xi, 0)
                            round_notnan_bkgd_bands_xi = np.floor(notnan_bkgd_bands_xi)
                            mode_val = stats.mode(round_notnan_bkgd_bands_xi)[0][0]
                            plt.axvline(x_mean, label="mean = %0.2f" % (x_mean), color="g")
                            plt.axvline(x_median, label="median = %0.2f" % (x_median), linestyle="-.", color="b")
                            plt.axvline(mode_val, label="mode = %0.2f" % (mode_val), color="r")
                            plt.legend()
                            print('Number of bins in histogram: ', len(bins))
                            print('Number of points used for histogram for column', xi,': ', len(notnan_bkgd_bands_xi))
                            plt.title("Background values for integration "+repr(i)+" and column "+repr(xi)+" \n")
                            plt.ylabel("N")
                            plt.xlabel("Background value [counts/sec]")
                            plt.grid(True, which='both')
                            plt.minorticks_on()
                            # bottom figure
                            ax = plt.subplot(212)
                            plt.plot(concat_bkgdvals_xi, y_bkgd_vals_xi, '.')
                            plt.axvline(x_mean, label="mean = %0.2f" % (x_mean), color="g")
                            plt.axvline(x_median, label="median = %0.2f" % (x_median), linestyle="-.", color="b")
                            plt.axvline(mode_val, label="mode = %0.2f" % (mode_val), color="r")
                            plt.legend()
                            plt.xlabel("Background value")
                            plt.ylabel("Y pixel ")
                            plt.grid(True, which='both')
                            plt.minorticks_on()
                            plt.show()
                            plt.close()
            if skip_bkgd_yidx_below:
                continue
        if band_height is None:
            # combine the values above and below
            bkgd_bands_concatenated = bkgd_values_above + bkgd_values_below
            bkgd_bands_concatenated = np.array(bkgd_bands_concatenated)
            bkgd_value = np.median(bkgd_bands_concatenated)
            mode_val = stats.mode(round_notnan_bkgd_bands)
            mode_freq = mode_val[1][0]
            bkgd_mode = mode_val[0][0]
        else:
            # remove the NaN values to estimate the background value
            nanidx_boolean = np.isnan(bkgd_bands)
            notnanidx = np.where(nanidx_boolean == False)
            if debug:
                notnanidx = notnanidx[0]
            notnan_bkgd_bands = bkgd_bands[notnanidx]  # only keep the non-nan values
            # round everything to 1 decimal
            round_notnan_bkgd_bands = np.round(notnan_bkgd_bands, 1)
            mode_val = stats.mode(round_notnan_bkgd_bands)
            #mode_freq = mode_val[1][0]
            #bkgd_mode = mode_val[0][0]
            # Change for ramps?
            mode_freq = mode_val[1]
            bkgd_mode = mode_val[0]
            x_mean = np.mean(notnan_bkgd_bands)
            x_median = np.median(notnan_bkgd_bands)
            # calculate standard deviation
            xstd = np.std(notnan_bkgd_bands)
            print(' Background band mean = ', x_mean)
            print(' Background band median (background value used) = ', x_median)
            print(' Background band standard deviation = ', xstd)
            print(' Mode = ', bkgd_mode)
            print(' Frequency of mode is ', mode_freq)

            # THIS IS OUR CHOSEN BACKGROUND VALUE
            bkgd_value = x_median

            if debug:
                # print some useful metrics
                print(' notnan_bkgd_bands = ', notnan_bkgd_bands, '  length = ', len(notnan_bkgd_bands))
                # do histogram
                plt.figure(1, figsize=(10, 8))
                plt.subplots_adjust(hspace=0.4)
                alpha = 0.2
                # top figure
                ax = plt.subplot(211)
                n, bins, patches = ax.hist(notnan_bkgd_bands, bins='auto', histtype='bar', ec='k', facecolor="blue", alpha=alpha)
                plt.axvline(x_mean, label="mean = %0.2f" % (x_mean), color="g")
                plt.axvline(x_median, label="median = %0.2f" % (x_median), linestyle="-.", color="b")
                plt.axvline(bkgd_mode, label="mode = %0.2f" % (bkgd_mode), color="r")
                plt.legend()
                print(' Number of bins in histogram: ', len(bins))
                print(' Number of points used for histogram: ', len(notnan_bkgd_bands))
                plt.title("Background values for integration "+repr(i)+" \n")
                plt.ylabel("N")
                plt.xlabel("Background value [counts/sec]")
                plt.xlim(-5*xstd, 5*xstd)
                plt.grid(True, which='both')
                plt.minorticks_on()
                # bottom figure
                ax = plt.subplot(212)
                plt.plot(concat_bkgdvals, y_bkgd_vals, '.')
                plt.axvline(x_mean, label="mean = %0.2f" % (x_mean), color="g")
                plt.axvline(x_median, label="median = %0.2f" % (x_median), linestyle="-.", color="b")
                plt.axvline(bkgd_mode, label="mode = %0.2f" % (bkgd_mode), color="r")
                plt.legend()
                plt.xlabel("Background value")
                plt.ylabel("Y pixel ")
                plt.xlim(-5*xstd, 5*xstd)
                plt.grid(True, which='both')
                plt.minorticks_on()
                plt.show()
                plt.close()
        print(' Estimated local background value for integration ', i, ' is', bkgd_value, '\n')
        bkgd_value_dict[i] = bkgd_value
        # record values in the background array
        bck_array[i, :, :] = bkgd_value
        if save_figs or show_figs:
            if i == 0 or i == int(nintegrations/2.0):
                # make sanity-check plot
                plt.figure(figsize=(10, 8))
                im = plt.imshow(masked_data[i])
                plt.colorbar()
                if band_height is not None:
                    plt.imshow(bkgd_bandabove, cmap='gray', alpha=0.5)
                    plt.imshow(bkgd_bandbelow, cmap='gray', alpha=0.5)
                # add to sanity-check plot
                plt.plot(trace_x[i], trace_y[i], color='red', lw=1, alpha=0.5)
                plt.plot(bkgd_valxidx_above, bkgd_valyidx_above, '.', color='blue', lw=1, alpha=0.5)
                plt.plot(bkgd_valxidx_below, bkgd_valyidx_below, '.', color='yellow', lw=1, alpha=0.5)
                plt.title('Points to be used to determine background value')
                plt.gca().invert_yaxis()  # so that axis has 0 at bottom left
                if save_figs:
                    if output_dir is None:
                        output_dir = ""
                    plt.savefig(os.path.join(output_dir, "bkgd_value_i"+repr(i)+".png"))
                if show_figs:
                    plt.show()
                plt.close()
        if debug:
            # break after the 2nd integration
            if i == 2:
                break
    print('\n Dictionary of background values per integration: ', repr(bkgd_value_dict))
    return bkgd_value_dict, bck_array


def save_json(output_dir, bkgd_value_dict):
    """
    Function to save the bacground values per integration into a json file.
    Author:
        Maria Pena-Guerrero (pena@stsci.edu)
    Returns:
        Nothing
    """
    if output_dir is None:
        output_dir = ""
    dict_to_be_converted_json_file = os.path.join(output_dir, 'bkgd_value_dict.json')
    with open(dict_to_be_converted_json_file, 'w') as json_file:
        json.dump(bkgd_value_dict, json_file)
    print('\n json file saved with background values at: ', dict_to_be_converted_json_file)


def subtract_bkgd(data_arr, bck_array, output_dir=None, save_figs=False, show_figs=False):
    """
    Function to subtract the bacground value from the input data and plot result
    Args:
        data_arr: array, pipeline TSO data i.e. 3 dimensions (integrations, rows, columns)
        bck_array: array, an array equal in size to the original data input, to make
                   background subraction easier
        output_dir: string or None, path where to place outputs. Default is same dir as input file
        save_figs: boolean, default is False
        show_figs: boolean, if True only the 0th and nintegrations/2 th plots will be show
    Author:
        Maria Pena-Guerrero (pena@stsci.edu)
    Returns:
        bkgdless_data: array of same dimensions as input with bacgound removed
    """
    bkgdless_data = data_arr - bck_array
    print('\n Background subtracted data array shape: ', np.shape(bkgdless_data))
    hdu = fits.PrimaryHDU(bkgdless_data)
    hdu.writeto('/Users/dlong/DataAnalysis/JWST/ahsoka/ahsoka_w39b_prism_dev/background_subtracted.fits', overwrite=True)
    if save_figs or show_figs:
        # make sanity-check plot
        plt.figure(figsize=(10, 8))
        plt.subplots_adjust(hspace=0.4)
        # Top figure
        ax = plt.subplot(211)
        plt.title("Data WITH background \n")
        im = plt.imshow(data_arr[0])
        #im.set_clim(-3.0e-9,6.5e-8)
        plt.gca().invert_yaxis()  # so that axis has 0 at bottom left
        plt.colorbar()
        # Bottom figure
        ax = plt.subplot(212)
        plt.title("Data background removed \n")
        im = plt.imshow(bkgdless_data[0])
        #im.set_clim(-3.0e-9,6.5e-8)
        plt.gca().invert_yaxis()  # so that axis has 0 at bottom left
        plt.colorbar()
        # add to sanity-check plot
        if save_figs:
            if output_dir is None:
                output_dir = ""
            plt.savefig(os.path.join(output_dir, "bkgdless_data.png"))
        if show_figs:
            plt.show()
        plt.close()
    return bkgdless_data


def mk_white_light_plot(time_tab, bkgd_masked, output_dir,
                        save_figs=True, show_figs=False, debug=False):
    """
    Function to make the white light curve.
    Args:
        bkgd_masked: array, input data array with background area masked
        output_dir: string or None, path where to place outputs. Default is same dir as input file
        save_figs: boolean, default is False
        show_figs: boolean, if True only the 0th and nintegrations/2 th plots will be show
        debug: boolean
    Author:
        Maria Pena-Guerrero (pena@stsci.edu)
    Returns:
        Nothing
    """
    if debug:
        save_figs = False
        show_figs = True
    # get the time array
    # table headers: integration_number, int_start_MJD_UTC, int_mid_MJD_UTC, int_end_MJD_UTC,
    #                int_start_BJD_TDB, int_mid_BJD_TDB, int_end_BJD_TDB
    time_arr = time_tab.field('int_start_MJD_UTC')
    # get the data in the masked out box only
    if debug:
        # sanity check
        plt.figure(figsize=(10, 8))
        plt.title('Data in the masked out box')
        im = plt.imshow(bkgd_masked[0])  # plotting only the 0th integration
        plt.gca().invert_yaxis()  # so that axis has 0 at bottom left
        if save_figs:
            if output_dir is None:
                output_dir = ""
            plt.savefig(os.path.join(output_dir, "spec_masked_bkg.png"))
        if show_figs:
            plt.show()
        plt.close()
    # create the white light array
    white_light = []
    nintegrations, rows, cols = np.shape(bkgd_masked)
    for ni in range(nintegrations):
        # get all the NOT nan indexes
        nanidx_boolean = np.isnan(bkgd_masked[ni])
        not_nanidx = np.where(nanidx_boolean == False)
        if debug:
            not_nanidx = not_nanidx[0]
        white_light.append(bkgd_masked[ni][not_nanidx].sum())
    if debug:
        print('white_light = ', white_light)

    # write a text file of this info
    if len(white_light) == len(time_arr):
        save_wl_file(output_dir, white_light, time_arr)
    else:
        print('\n WARNING: white light text file NOT written because arrays have different lengths')
    # plot
    plt.figure(figsize=(10, 8))
    plt.title("White Light Curve \n")
    # check that there is something in the table (in case of simulations)
    if len(time_arr) == 0:
        print('\n * WARNING: The integrations times table is not filled, only plotting points')
        plt.plot(white_light, '.')
        plt.xlabel("Integrations")
    else:
        plt.plot(time_arr, white_light, '.')
        plt.xlabel("Time [int_start_MJD_UTC]")
    plt.ylabel("Flux [counts/sec]")
    plt.grid(True, which='both')
    plt.minorticks_on()
    if save_figs:
        if output_dir is None:
            output_dir = ""
        plt.savefig(os.path.join(output_dir, "white_light.png"))
    if show_figs:
        plt.show()
    plt.close()


def save_wl_file(output_dir, white_light, time_arr):
    """
    Function to writhe the white light curve in a text file.
    Args:
        output_dir: string or None, path where to place outputs. Default is same dir as input file
        white_light: array, summed flux over the mask box created in the background function
        time_arr: array, time used for the white light curve
    Author:
        Maria Pena-Guerrero (pena@stsci.edu)
    Returns:
        Nothing
    """
    wl_file = os.path.join(output_dir, 'white_light.txt')
    with open(wl_file, "w+") as wlf:
        hdr = "{:<13} {:<20} {:<20}".format("# Integration", "Flux [counts/sec]", "Time [[int_start_MJD_UTC]]")
        wlf.write(hdr + "\n")
        for i, t in enumerate(time_arr):
            line = "{:<13} {:<20} {:<20}".format(i, white_light[i], t)
            wlf.write(line + "\n")
    print("\n White light text table saved at: ", wl_file)


def rm_background(data_path, output_dir=None, spectrum_width=None, tracefind=None,
                  background_function=None, band_height=None,
                  save_figs=True, show_figs=False, debug=False):
    """
    Work horse function of this script. The general idea follows this recipy:
    1. Find the trace
    2. Mask out the area of the source spectrum
    3. Use local background estimation method to obtain background value
    4. Subtract background value from all pixels

    Author:
        Maria Pena-Guerrero (pena@stsci.edu)

    Agrs:
        data_path: string, path of input file (rateints-like, i.e. data shape has 3 values)
        output_dir: string or None, path where to place outputs. Default is same dir as input file
        spectrum_width: integer, full width of spectrum in pixels
        tracefind: string, default is to use a spline
            other accepted values:
            'nonparam' - uses the non-parametric function written by N. Espinoza
            'poly' - uses a polynomial to find the trace
        background_function: str or None, background function to use, default is Webb
        band_height: None, integer, or 'all' - height of background height to use
        save_figs: boolean, default is False
        show_figs: boolean, default is True
        debug: boolean, defult is False, if True a series of mesages will be printed on-screen

    Returns:
        Nothing. The final data with the subtracted background will be written in a new fits file.
    """

    if debug:
        save_figs = False
        show_figs = True

    # start the timer
    start_time = time.time()

    # read the file and get the shape
    with fits.open(data_path) as hdul:
        hdr = hdul[0].header
        data_arr = hdul['SCI'].data
        dq_array = hdul['DQ'].data
        time_tab = hdul['INT_TIMES'].data

    # remove reference pixels, if any
    data_copy = rm_ref_pix(data_arr)

    # STEP 1 - Find the trace
    if tracefind == 'spline':
        print('\nUsing spline to find traces... \n')
        trace_x, trace_y = spline_tracefind(data_copy, n_interior_knots=10, output_dir=output_dir,
                                            save_figs=save_figs, show_figs=show_figs, debug=debug)
    elif tracefind is None or tracefind == 'poly':
        print('\nUsing polynomial to find traces... \n')
        trace_x, trace_y = poly_tracefind(data_copy, max_order=30, output_dir=output_dir,
                                          save_figs=save_figs, show_figs=show_figs, debug=debug)
    elif tracefind == 'nonparam':
        print('\nUsing non-parametric function to find traces... \n')
        trace_x, trace_y = nonparam_tracefind(data_arr, dq_array, instrument='nirspec',
                                              output_dir=output_dir, save_figs=save_figs,
                                              show_figs=show_figs, debug=debug)

    if background_function is None or 'w' in background_function.lower():
        # STEP 2 - Mask out area of spectrum
        print('masking spectrum...')
        masked_data, bkgd_masked = mask_spec(data_copy, trace_x, trace_y, spectrum_width=spectrum_width,
                                             output_dir=output_dir, save_figs=save_figs,
                                             show_figs=show_figs, debug=debug)

        # STEP 3 - Estimate background
        print('calculating background with function created for Webb...')
        bkgd_value_dict, bck_array = get_background(trace_x, trace_y, masked_data,
                                                    height_from_spec=5, band_height=band_height,
                                                    output_dir=output_dir, save_figs=save_figs,
                                                    show_figs=show_figs, debug=debug)
    else:
        # STEPS 2 and 3 combined here
        print('calculating background with function creted for HST...')
        top_ap, low_ap = hdr['SUBSIZE2'], 0
        bkgd_value_dict, bck_array, bkgd_masked = background_wrapper(data_copy, top_ap, low_ap,
                                                                     output_dir=output_dir,
                                                                     save_figs=save_figs,
                                                                     show_figs=show_figs, debug=debug)
    # write the info in a file
    save_json(output_dir, bkgd_value_dict)

    # bonus step - produce white light curve
    print('producing white light curve...')
    mk_white_light_plot(time_tab, bkgd_masked, output_dir=output_dir,
                        save_figs=save_figs, show_figs=show_figs, debug=debug)

    # STEP 4 - Subtract the background from the input image
    print('subracting background...')
    bkgdless_data = subtract_bkgd(data_arr, bck_array, output_dir=output_dir,
                                  save_figs=save_figs, show_figs=show_figs)

    # end the timer and report
    end_time = end_timer(start_time)

    print('\n * Script rm_background.py finished in ', end_time, ' \n')
