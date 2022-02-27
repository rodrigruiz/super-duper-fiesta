import numpy as np
import km3io

def get_by_range(e, emin, emax):
    '''
    Given an input energy corresponding to the energy of the interacting neutrino, this function returns a
    range of the inelasticity parameter by which corresponds to a cascade energy between 90 and 110 TeV.
    Keyword arguments:
    e -- the primary neutrino energy
    emin -- minimum energy of the cascade
    emax -- maximum energy of the cascade

    Returns a 1d array with two elements, [ymin, ymax]:
    ymin is the inelasticity corresponding to e and emin
    ymax is the inelasticity corresponding to e and emax

    '''
    E_nu = x
    E_cascade = np.array([emin,emax])
    E_nu_prime = E_nu - E_cascade
    y = (E_nu - E_nu_prime)/E_nu
    return y

def extract_data(f):
    """
    Reads a gSeaGen file (km3net-dataformat), and extracts primary neutrino energies and by for each event. 
    Keyword arguments:
    f -- path to a gSeaGen file
    Returns a dictionary with the following keys:
    by -- Inelasticity
    e -- primary neutrino energy
    loge -- log10(e)
    logby -- log10(by)
    """
    f = km3io.OfflineReader(f)
    d = {}
    BY_IDX=km3io.definitions.w2list_gseagen.W2LIST_GSEAGEN_BY
    d['by']    = np.array(f.events.w2list[:,BY_IDX])
    d['e']     = np.array(f.events.mc_trks.E[:,0])
    d['loge']  = np.log10(d['e'])
    d['logby'] = np.log10(d['by'])
    return d
