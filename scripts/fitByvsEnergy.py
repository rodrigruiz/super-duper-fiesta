"""
Usage: fitByvsEnergy.py -i INPUT_FILE -f FLAVOR -c CHANNEL -e E_MIN -E E_MAX -t JSON_TABLE

Options:
  -h --help                      Help.
  -i --input_file INPUT_FILE     Input file.  
  -f --flavor FLAVOR             Neutrino flavor (nu_e, nu_mu, nu_e_bar, nu_mu_bar). 
  -c --channel CHANNEL           Interaction channel (cc nc).
  -e --emin E_MIN                Minimum cascade energy.  
  -E --emax E_MAX                Maximum cascade energy.
  -t --json_table JSON_TABLE     JSON formatted table with all the analysis parameters.  
"""

from docopt import docopt
from fiesta import tools as tls
from fiesta import table as tbl
from os.path import exists
import glob, os
import pickle as pkl
import numpy as np
from fiesta import nuBy as nb
import boost_histogram as bh
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from pathlib import Path
import json

def main():
    arguments = docopt(__doc__)

    flavors =["nu_e", "nu_mu", "anu_e", "anu_mu"]
    channels=["cc", "nc"]
    
    if (arguments['--flavor'] not in flavors):
        print('ERROR: Flavor argument must be from the list:\n ', flavors)
        exit(1)

    if (arguments['--channel'] not in channels):
        print('ERROR: Channel argument must be from the list:\n ', channels)
        exit(1)

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
        y1,y2 = nb.get_by_range(e, float(arguments['--emin']), float(arguments['--emax']))
        p = tls.integrate_x_range(pdf,y1,y2)
        en.append(e)
        pr.append(p)

    a,b = curve_fit(nb.p_100TeV, en[2:], pr[2:], maxfev=2000)

    t = tbl.table.from_json(arguments["--json_table"])
    t.set_proba(arguments['--flavor']+'_'+arguments['--channel'], arguments['--emin'], arguments['--emax'], a[0], a[1])
    t.write(arguments["--json_table"])
    
if __name__== '__main__':
    main()

    
