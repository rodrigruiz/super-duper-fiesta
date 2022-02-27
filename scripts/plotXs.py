"""
Usage: plotXs.py [-o OUTPUT_FILE] -p PARAMETER_FILE -x XS_FILE

Options:
  -h --help                           Help.
  -o --output_file OUTPUT_FILE        Output file.
  -p --parameter_file PARAMETER_FILE  Input file.
  -x --xs_file XS_FILE                Xs file. 
"""

from docopt import docopt
from pathlib import Path
from fiesta import nuXs as nx
from fiesta import tools as tls
from scipy.optimize import curve_fit
from os.path import exists
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import json

def main():
    arguments = docopt(__doc__)

    if (arguments['--output_file']==None):
        arguments['--output_file']=Path(arguments['--xs_file']).stem+'.png'

    with open(arguments["--parameter_file"], 'r') as json_file:
        p = json.load(json_file)
    json_file.close()
        
    xs=nx.read_xs_file(arguments["--xs_file"])
    
    fig1, axs1 = plt.subplots(2, 2)
    fig1.set_size_inches(10,7)

    
    
    # panel 1: cc nu
    axs1[0, 0].plot(xs["log_E"], xs["cc_nu"], color='darkorange', label='data')
    axs1[0, 0].plot(xs["log_E"][650:],
                   nx.dis_xs(xs["log_E"][650:], p["cc_nu"]["a1"], p["cc_nu"]["b1"], p["cc_nu"]["a2"], p["cc_nu"]["b2"]),
                   color='grey', label='fit')
    axs1[0, 0].set_title(r'$\sigma_{\nu} CC$')

    # panel 2: nc nu
    axs1[0, 1].plot(xs["log_E"], xs["nc_nu"], color='darkorange', label='data')
    axs1[0, 1].plot(xs["log_E"][650:],
                   nx.dis_xs(xs["log_E"][650:], p["nc_nu"]["a1"], p["nc_nu"]["b1"], p["nc_nu"]["a2"], p["nc_nu"]["b2"]),
                   color='grey', label='fit')
    axs1[0, 1].set_title(r'$\sigma_{\nu} NC$')

    # panel 3: electron antineutrinos
    axs1[1, 0].plot(xs["log_E"], xs["cc_nu_bar"], color='darkorange', label='data')
    axs1[1, 0].plot(xs["log_E"][650:],
                   nx.dis_xs(xs["log_E"][650:], p["cc_nu_bar"]["a1"], p["cc_nu_bar"]["b1"], p["cc_nu_bar"]["a2"], p["cc_nu_bar"]["b2"]),
                   color='grey', label='fit')
    axs1[1, 0].set_title(r'$\sigma_{\bar{\nu}} CC$')

    # panel 4: muon antineutrinos
    axs1[1, 1].plot(xs["log_E"], xs["nc_nu_bar"], color='darkorange', label='data')
    axs1[1, 1].plot(xs["log_E"][650:],
                   nx.dis_xs(xs["log_E"][650:], p["nc_nu_bar"]["a1"], p["nc_nu_bar"]["b1"], p["nc_nu_bar"]["a2"], p["nc_nu_bar"]["b2"]),
                   color='grey', label='fit')
    axs1[1, 1].set_title(r'$\sigma_{\bar{\nu}} NC$')

    # general settings for all the panels
    for ax in [axs1[1, 0], axs1[1, 1]]:
        ax.set(xlabel='log10(E/GeV)')
        
    for ax in [axs1[0, 0], axs1[1, 0]]:
        ax.set(ylabel=r'$\sigma$/$cm ^{2}$')

    for ax in axs1.flatten():
        ax.grid()
        ax.legend()
        ax.set_yscale('log')

    fig1.savefig('nu_XS.png', dpi=fig1.dpi)
    
    # plt.show()
        
if __name__== '__main__':
    main()
