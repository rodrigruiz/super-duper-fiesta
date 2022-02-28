import numpy as np
import boost_histogram as bh
import matplotlib
import matplotlib.pyplot as plt

def find_nearest_index(array, value):
    """
    Given an array and a value, this function returns the index of the element in the array closest to the value.
    
    Keyword arguments:
    array -- the numpy array
    value -- the value
    """
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def get_x_pdf(hist2d, bin_number):
    '''
    This function receives a 2D boost histogram and returns a dictionary corresponing to a pdf for a given bin on the x axis.

    Keyword arguments:
    array -- hist2d, a 2d boost histogram
    bin_number -- the index of the x-axis bin that will be sliced

    Returns a dictionary has the following keys:
    volumes: bin widths
    density: bin values
    centres: bin centres
    '''
    h1d = hist2d[bin_number, :]
    d = {}
    volumes = np.prod(h1d.axes.widths, axis=0)
    density = h1d.view() / h1d.sum() / volumes
    d['density'] = density
    d['volumes'] = volumes
    d['centres'] = h1d.axes.centers[0]
    return d

def integrate_bin_range(h,a,b):
    '''
    Returns the integral of a 1D histogram between bin indices a and b.

    Keyword arguments:
    h -- 1d histogram (dictionary) with the following keys:
    volumes: bin widths
    density: bin values
    centres: bin centres
    a -- lower bin index
    b -- higher bin index
    '''
    integral=0.
    if(len(h['volumes'][a:b])==len(h['density'][a:b])):
        for i, (c,w) in enumerate(zip(h['density'][a:b],h['volumes'][a:b])):
            integral = integral+c*w
    return integral

def integrate_x_range(h,a,b):
    '''
    Returns the integral of a 1D histogram between abscisa values a and b.

    Keyword arguments:
    h -- 1d histogram (dictionary) with the following keys:
    volumes: bin widths
    density: bin values
    centres: bin centres
    a -- lower abscissa value
    b -- higher abscissa value
    '''
    integral=0.
    if(len(h['volumes'])==len(h['density'])):
        i = find_nearest_index(h['centres'], a)
        j = find_nearest_index(h['centres'], b)
        for i, (c,w) in enumerate(zip(h['density'][i:j],h['volumes'][i:j])):
            integral = integral+c*w
    return integral

def plot_2d_hist(h):    
    w,x,y = h.to_numpy()
    fig, ax = plt.subplots()
    mesh = ax.pcolormesh(x, y, w.T,norm=matplotlib.colors.LogNorm())
    ax.set_xlabel(h.axes[0].metadata)
    ax.set_ylabel(h.axes[1].metadata)
    fig.colorbar(mesh)
    return fig,ax
