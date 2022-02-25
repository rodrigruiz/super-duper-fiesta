import numpy as np

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
