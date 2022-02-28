"""
Usage: fitByvsEnergy.py [-o OUTPUT_FILE] -i INPUT_FILE -f FLAVOR -c CHANNEL -e E_MIN -E E_MAX

Options:
  -h --help                      Help.
  -o --output_file OUTPUT_FILE   Output file.
  -i --input_file INPUT_FILE     Input file.  
  -f --flavor FLAVOR             Neutrino flavor (nu_e, nu_mu, nu_e_bar, nu_mu_bar). 
  -c --channel CHANNEL           Interaction channel (cc nc).
  -e --emin E_MIN                Minimum cascade energy.  
  -E --emax E_MAX                Maximum cascade energy.  
"""

from docopt import docopt
from fiesta import tools as tls
from os.path import exists
import glob, os
import pickle as pkl
import numpy as np
from fiesta import nuBy as nb
import boost_histogram as bh
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def main():
    arguments = docopt(__doc__)

    flavors =["nu_e", "nu_mu", "nu_e_bar", "nu_mu_bar"]
    channels=["cc", "nc"]
    
    if (arguments['--flavor'] not in flavors):
        print('ERROR: Flavor argument must be from the list:\n ', flavors)
        exit(1)

    if (arguments['--channel'] not in channels):
        print('ERROR: Channel argument must be from the list:\n ', channels)
        exit(1)

    if (arguments['--output_file']==None):
        arguments['--output_file']=arguments["--flavor"]+"_"+arguments["--channel"]+"_by_vs_E.png"
    

    pickle_file=open(arguments["--input_file"], 'rb')
    histograms=pkl.load(pickle_file)
    pickle_file.close()
    
    h=histograms[arguments["--flavor"]+"_"+arguments["--channel"]]
    energies=h.axes.centers[0].flatten()
    en=[]
    pr=[]
    idx=tls.find_nearest_index(energies, 1e5)
    for i, e in enumerate(energies[idx:-2]):
        pdf=tls.get_x_pdf(h,i+idx)
        y1,y2 = nb.get_by_range(e, 9e4, 1.1e5)
        p = tls.integrate_x_range(pdf,y1,y2)
        en.append(e)
        pr.append(p)

    a,b = curve_fit(nb.p_100TeV, en[2:], pr[2:], maxfev=2000)
    plt.plot(en[2:], nb.p_100TeV(en[2:], a[0], a[1]), label='Fit')
    plt.plot(en[2:],pr[2:], label="data")
    plt.yscale("log")
    plt.xscale("log")
    plt.xlabel("Neutrino energy(GeV)")
    plt.ylabel("P(90TeV-110TeV)")
    plt.legend()
    plt.show()
    
if __name__== '__main__':
    main()

    
