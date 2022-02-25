import numpy as np

def read_flux_file(f):
    """Read file with atmospherix flux data.
    This file contains 5 columns:
    column1 -- log10(E/GeV)
    column2 -- F(nu_e)/(m^-2*s^-1)
    column2 -- F(nu_mu)/(m^-2*s^-1)
    column2 -- F(nu_e_bar)/(m^-2*s^-1)
    column2 -- F(nu_mu_bar)/(m^-2*s^-1)

    Keyword arguments:
    f -- path to the file

    Returns a dictionary with the following elements (a factor is applied to convert units to cm^-2*s^-1*sr^-1):
    d["log_E"]=np.array(log_e)
    d["E"]=np.power(10, np.array(log_e))
    d["nu_e"]=np.array(nue)
    d["nu_mu"]=np.array(numu)
    d["nu_e_bar"]=np.array(nuebar)
    d["nu_mu_bar"]=np.array(numubar)
    """
    d={}
    units_factor = 1.e-4/(4*np.pi) "from m^-2 to cm^-2, and from full solid angle to sr^-1"
    log_e, nue, numu, nuebar, numubar = ([] for i in range (5))
    File = open(f,"r")
    lines = File.readlines()
    for line in lines:
        columns = line.split(' ')
        log_e.append(float(columns[0]))
        nue.append(float(columns[1])*units_factor)
        numu.append(float(columns[2])*units_factor)
        nuebar.append(float(columns[3])*units_factor)
        numubar.append(float(columns[4])*units_factor)
    d["log_E"]=np.array(log_e)
    d["E"]=np.power(10, np.array(log_e))
    d["nu_e"]=np.array(nue)
    d["nu_mu"]=np.array(numu)
    d["nu_e_bar"]=np.array(nuebar)
    d["nu_mu_bar"]=np.array(numubar)
    File.close()
    return d

def ic_flux(x, phi, gamma, E0, C0):
    """Returns astrophysical neutrino flux following the model reported on https://arxiv.org/pdf/2001.09520.pdf. Units are cm^-2*s^-1*sr^-1
    
    Keyword arguments:
    x -- energy
    phi -- flux normalisation
    gamma -- spectral index
    E0 -- Reference energy
    C0 -- Reference constant
    """
    return C0 * phi * np.power((x/E0), -gamma)

def atm_flux(x, phi, gamma):
    """Returns atmospheric neutrino flux following a simple power law model, F = phi*power((x), -gamma). Units are cm^-2*s^-1*sr^-1
    
    Keyword arguments:
    x -- energy
    phi -- flux normalisation
    gamma -- spectral index
    """
    return phi * np.power((x), -gamma)
