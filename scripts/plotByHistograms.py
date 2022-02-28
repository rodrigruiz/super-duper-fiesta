"""
Usage: plotByHistograms.py [-o OUTPUT_FILE] -i INPUT_FILE -f FLAVOR -c CHANNEL

Options:
  -h --help                      Help.
  -o --output_file OUTPUT_FILE   Output file.
  -i --input_file INPUT_FILE     Input file.  
  -f --flavor FLAVOR             Neutrino flavor (nu_e, nu_mu, nu_e_bar, nu_mu_bar). 
  -c --channel CHANNEL           Interaction channel (cc nc).
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

    fig, ax= tls.plot_2d_hist(h)

    emin=9e4
    emax=1.1e5
    ymin=[]
    ymax=[]
    logE_min = 5.0
    logE_max = 8.0
    N_e = 100
    step_e = (logE_max - logE_min)/N_e
    logE = np.arange(logE_min,logE_max+step_e,step_e)
    E = np.power(10,logE)
    for e in E:
        yrange = nb.get_by_range(e, emin, emax)
        ymin.append(yrange[0])
        ymax.append(yrange[1])

    ax.plot(E,ymin, color='white')
    ax.plot(E,ymax, color='white')
    ax.set_xlabel("Neutrino energy(GeV)")
    ax.set_ylabel("Inelasticity y")
    ax.set_yscale("log")
    ax.set_xscale("log")

    fig.savefig(arguments['--output_file'], dpi=fig.dpi)

    # plt.show()
    
if __name__== '__main__':
    main()
