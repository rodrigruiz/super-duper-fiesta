import numpy as np

def read_xs_file(f):
    """
    Read atmospheric neutrino fluxes from an asscii file.

    The file is organised in 5 columns as follows:
    column1 -- log10(E/GeV)
    column2 -- sigma_cc(nu)/(cm^-2)
    column3 -- sigma_nc(nu)/(cm^-2)
    column4 -- sigma_cc(nu_bar)/(cm^-2)
    column5 -- sigma_nc(nu_bar)/(cm^-2)

    Keyword arguments:
    f -- the path to the file

    Returns a dictionary with the following keys (cross sections are given in cm^-2):
    d["log_E"]=np.array(log_e) log10(GeV)
    d["E"]=np.power(10, np.array(log_e)) GeV
    d["cc_nu"]=np.array(nue)
    d["nc_nu"]=np.array(numu)
    d["cc_nu_bar"]=np.array(nuebar)
    d["nc_nu_bar"]=np.array(numubar)
    """
    d={}
    log_e, cc_nu, nc_nu, cc_nu_bar, nc_nu_bar = ([] for i in range(5))
    File = open(f,"r")
    lines = File.readlines()
    for line in lines:
        columns = line.split(' ')
        log_e.append(float(columns[0]))
        cc_nu.append(float(columns[1]))
        nc_nu.append(float(columns[2]))
        cc_nu_bar.append(float(columns[3]))
        nc_nu_bar.append(float(columns[4]))
    d["log_E"]=np.array(log_e)
    d["E"]=np.power(10, np.array(log_e))
    d["cc_nu"]=np.array(cc_nu)
    d["nc_nu"]=np.array(nc_nu)
    d["cc_nu_bar"]=np.array(cc_nu_bar)
    d["nc_nu_bar"]=np.array(nc_nu_bar)
    File.close()
    return d

def dis_xs(x, a1, b1, a2, b2):
    """
    Returns a model for the deep inelastic cross section above 10^5 GeV. This model represents the cross section as a broken exponential function. The breaking energy is set for simplicity at 10^8 GeV 
    Keyword arguments:
    le -- log10(energy/GeV)
    a1 -- normalisation for the range 10^5GeV < E < 10^8GeV
    b1 -- exponent for the range 10^5GeV < E < 10^8GeV
    a2 -- normalisation for the range  10^8GeV <= E
    b2 -- exponent for the range 10^8GeV <= E
    """
    return np.piecewise(x, [x < 8, x >= 8], [lambda x : np.exp(a1 + x*b1), lambda x : np.exp(a2 + x*b2)])
