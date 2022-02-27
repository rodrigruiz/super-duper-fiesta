"""
Usage: plotAtmFlux.py [-o OUTPUT_FILE] -p PARAMETER_FILE -f FLUX_FILE

Options:
  -h --help                           Help.
  -o --output_file OUTPUT_FILE        Output file.
  -p --parameter_file PARAMETER_FILE  Input file.
  -f --flux_file FLUX_FILE            Flux file. 
"""

from docopt import docopt
from pathlib import Path
from fiesta import nuFlux as nf
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
        arguments['--output_file']=Path(arguments['--flux_file']).stem+'.png'


    with open(arguments["--parameter_file"], 'r') as json_file:
        p = json.load(json_file)
    json_file.close()
        
    flux=nf.read_flux_file(arguments["--flux_file"])

    phi=1.66
    gamma=2.53
    e0=100e3
    c0=3e-18
    
    fig1, axs1 = plt.subplots(2, 2)
    fig1.set_size_inches(10,7)

    # panel 1: electron neutrinos
    axs1[0, 0].plot(flux["E"], flux["nu_e"], color='darkorange', label='atmospheric')
    axs1[0, 0].plot(flux["E"][600:],
                   nf.atmospheric_flux(flux["E"][600:], p["nu_e"]["phi"], p["nu_e"]["gamma"]),
                   color='grey', label='fit')
    axs1[0, 0].set_title(r'$\nu_{e}$')

    # panel 2: muon neutrinos
    axs1[0, 1].plot(flux["E"], flux["nu_mu"], color='darkorange', label='atmospheric')
    axs1[0, 1].plot(flux["E"][600:],
                   nf.atmospheric_flux(flux["E"][600:], p["nu_mu"]["phi"], p["nu_mu"]["gamma"]),
                   color='grey', label='fit')
    axs1[0, 1].set_title(r'$\nu_{\mu}$')

    # panel 3: electron antineutrinos
    axs1[1, 0].plot(flux["E"], flux["nu_e_bar"], color='darkorange', label='atmospheric')
    axs1[1, 0].plot(flux["E"][600:],
                   nf.atmospheric_flux(flux["E"][600:], p["nu_e_bar"]["phi"], p["nu_e_bar"]["gamma"]),
                   color='grey', label='fit')
    axs1[1, 0].set_title(r'$\bar{\nu}_{e}$')

    # panel 4: muon antineutrinos
    axs1[1, 1].plot(flux["E"], flux["nu_mu_bar"], color='darkorange', label='atmospheric')
    axs1[1, 1].plot(flux["E"][600:],
                   nf.atmospheric_flux(flux["E"][600:], p["nu_mu_bar"]["phi"], p["nu_mu_bar"]["gamma"]),
                   color='grey', label='fit')
    axs1[1, 1].set_title(r'$\bar{\nu}_{\mu}$')

    # general settings for all the panels
    for ax in [axs1[1, 0], axs1[1, 1]]:
        ax.set(xlabel='log10(E/GeV)')
        
    for ax in [axs1[0, 0], axs1[1, 0]]:
        ax.set(ylabel=r'F$_{\nu}$/($GeV ^{-1} \cdot cm ^{-2}\cdot s ^{-1}\cdot sr ^{-1}$)')

    for ax in axs1.flatten():
        ax.grid()
        ax.plot(flux["E"], nf.astro_flux(flux["E"], phi, gamma, e0, c0)/6,
                   color='royalblue', label='astro')
        ax.legend()
        ax.set_yscale('log')
        ax.set_xscale('log')

    # figure showing all fluxes. The astro flux, is the total one (i.e. we don't divide by 6 to get the individual contributions)
    log_Emin = 2.0
    log_Emax = 12.0
    nPoints = 2000
    step=(log_Emax-log_Emin)/nPoints
    logE=np.arange(log_Emin, log_Emax, step)
    
    fig2, axs2 = plt.subplots(1,2)
    fig2.set_size_inches(11,4)
    
    # astro
    axs2[0].plot(np.power(10,logE), nf.astro_flux(np.power(10,logE), phi, gamma, e0, c0)/6, color='royalblue', label=r'astro $\nu _{i}$', linewidth=2)
    axs2[1].plot(np.power(10,logE), nf.astro_flux(np.power(10,logE), phi, gamma, e0, c0), color='royalblue', label=r'astro total', linewidth=2, alpha=1)
    
    # atm nu_e fit
    axs2[0].plot(np.power(10,logE)[700:],
                   nf.atmospheric_flux(np.power(10,logE)[700:], p["nu_e"]["phi"], p["nu_e"]["gamma"]),
                   color='darkorange', linestyle='--', alpha=0.7)
    
    # atm nu_e data
    axs2[0].plot(flux["E"][:800],
                   nf.atmospheric_flux(flux["E"][:800], p["nu_e"]["phi"], p["nu_e"]["gamma"]),
                   color='darkorange', linestyle='-', alpha=1, label=r'$\nu_{e}$')

    # atm nu_mu fit
    axs2[0].plot(np.power(10,logE)[700:],
                   nf.atmospheric_flux(np.power(10,logE)[700:], p["nu_mu"]["phi"], p["nu_mu"]["gamma"]),
                   color='limegreen', linestyle='--', alpha=0.7)

    # atm nu_mu data
    axs2[0].plot(flux["E"][:800],
                   nf.atmospheric_flux(flux["E"][:800], p["nu_mu"]["phi"], p["nu_mu"]["gamma"]),
                   color='limegreen', linestyle='-', alpha=1, label=r'$\nu_{\mu}$')

    # atm nu_e_bar fit
    axs2[0].plot(np.power(10,logE)[700:],
                   nf.atmospheric_flux(np.power(10,logE)[700:], p["nu_e_bar"]["phi"], p["nu_e_bar"]["gamma"]),
                   color='red', linestyle='--', alpha=0.7)
    # atm nu_e_bar data
    axs2[0].plot(flux["E"][:800],
                   nf.atmospheric_flux(flux["E"][:800], p["nu_e_bar"]["phi"], p["nu_e_bar"]["gamma"]),
                   color='red', linestyle='-', alpha=1, label=r'$\bar{\nu}_{e}$')

    # atm nu_mu_bar fit
    axs2[0].plot(np.power(10,logE)[700:],
                   nf.atmospheric_flux(np.power(10,logE)[700:], p["nu_mu_bar"]["phi"], p["nu_mu_bar"]["gamma"]),
                   color='olivedrab', linestyle='--', alpha=0.7)
    # atm nu_mu_bar data
    axs2[0].plot(flux["E"][:800],
                   nf.atmospheric_flux(flux["E"][:800], p["nu_mu_bar"]["phi"], p["nu_mu_bar"]["gamma"]),
                   color='olivedrab', linestyle='-', alpha=1, label=r'$\bar{\nu}_{\mu}$')

    # atm total data
    axs2[1].plot(flux["E"][:800],
              nf.atmospheric_flux(flux["E"][:800], p["nu_e"]["phi"], p["nu_e"]["gamma"])+
              nf.atmospheric_flux(flux["E"][:800], p["nu_mu"]["phi"], p["nu_mu"]["gamma"])+
              nf.atmospheric_flux(flux["E"][:800], p["nu_e_bar"]["phi"], p["nu_e_bar"]["gamma"])+
              nf.atmospheric_flux(flux["E"][:800], p["nu_mu_bar"]["phi"], p["nu_mu_bar"]["gamma"]),
              color='darkorange', linestyle='-', linewidth=2, alpha=1, label=r'atmospheric')

    # atm total fit
    axs2[1].plot(np.power(10,logE)[700:],
              nf.atmospheric_flux(np.power(10,logE)[700:], p["nu_e"]["phi"], p["nu_e"]["gamma"])+
              nf.atmospheric_flux(np.power(10,logE)[700:], p["nu_mu"]["phi"], p["nu_mu"]["gamma"])+
              nf.atmospheric_flux(np.power(10,logE)[700:], p["nu_e_bar"]["phi"], p["nu_e_bar"]["gamma"])+
              nf.atmospheric_flux(np.power(10,logE)[700:], p["nu_mu_bar"]["phi"], p["nu_mu_bar"]["gamma"]),
              color='darkorange', linestyle='--', linewidth=2, alpha=1)
    
    for ax in [axs2[0], axs2[1]]:
        ax.set(xlabel='log10(E/GeV)')
        ax.set_yscale('log')
        ax.set_xscale('log')
        ax.grid()
        ax.legend()

    for ax in [axs2[0]]:
        ax.set(ylabel=r'F$_{\nu}$/($GeV ^{-1} \cdot cm ^{-2}\cdot s ^{-1}\cdot sr ^{-1}$)')

    fig1.savefig('nu_flux_1.png', dpi=fig1.dpi)
    fig2.savefig('nu_flux_2.png', dpi=fig2.dpi)
    
    # plt.show()
        
if __name__== '__main__':
    main()
