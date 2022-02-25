import numpy as np

def read_flux_file(f):
    """
    Read atmospheric neutrino fluxes from an asscii file.

    The file is organised in 5 columns as follows:
    column1 -- log10(E/GeV)
    column2 -- F(nu_e)/(s^-1*m^-2)
    column3 -- F(nu_mu)/(s^-1*m^-2)
    column4 -- F(nu_e_bar)/(s^-1*m^-2)
    column5 -- F(nu_mu_bar)/(s^-1*m^-2)

    Keyword arguments:
    f -- the path to the file

    Returns a dictionary with the following keys (a conversion factor is applied so that the flux units are s^-1*cm^-2*sr^-1):
    d["log_E"]=np.array(log_e) log10(GeV)
    d["E"]=np.power(10, np.array(log_e)) GeV
    d["nu_e"]=np.array(nue)
    d["nu_mu"]=np.array(numu)
    d["nu_e_bar"]=np.array(nuebar)
    d["nu_mu_bar"]=np.array(numubar)
    """
    d={}
    log_e, nue, numu, nuebar, numubar = ([] for i in range (5))
    File = open(f,"r")
    lines = File.readlines()
    for line in lines:
        columns = line.split(' ')
        log_e.append(float(columns[0]))
        nue.append(float(columns[1]))
        numu.append(float(columns[2]))
        nuebar.append(float(columns[3]))
        numubar.append(float(columns[4]))
    d["log_E"]=np.array(log_e)
    d["E"]=np.power(10, np.array(log_e))
    d["nu_e"]=np.array(nue)
    d["nu_mu"]=np.array(numu)
    d["nu_e_bar"]=np.array(nuebar)
    d["nu_mu_bar"]=np.array(numubar)
    File.close()
    return d

def astro_flux(e, phi, gamma, e0, c0):
    """
    Returns the astrophysical neutrino flux in units of s^-1*cm^-2*sr^-1. This follows the parameterisation described in https://arxiv.org/pdf/2001.09520.pdf.

    Keyword arguments:
    e -- energy
    phi -- flux normalisation
    gamma -- spectral index
    e0 -- reference energy
    c0 -- reference normalisation
    """
    return c0 * phi * np.power((e/e0), -gamma)

def atmospheric_flux(e, phi, gamma, e0, c0):
    """
    Returns the atmospheric neutrino flux parametrised according to a simple power law, in units of s^-1*cm^-2*sr^-1.

    Keyword arguments:
    e -- energy
    phi -- flux normalisation
    gamma -- spectral index
    """
    return phi * np.power((e), -gamma)
