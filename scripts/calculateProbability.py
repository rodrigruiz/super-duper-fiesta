"""
Usage: calculateProbability.py [-A ATM_DATA -X XS_DATA -P PROB_DATA] -o OUT_FILE -t JSON_TABLE

Options:
  -h --help                            Help.
  -A --atm_flux_data ATM_DATA   JSON file with the atmospheric flux parameterisation.
  -X --xs_data XS_DATA    JSON file with the cross section parameterisation.  
  -P --prob_data PROB_DATA  JSON file with the parameterisation of the probability to get a 100TeV shower.
  -o --output_file OUT_FILE JSON file with the results.
  -t --json_table JSON_TABLE     JSON formatted table with all the analysis parameters.
"""
# """
# Usage: calculateProbability.py [-A ATM_DATA -X XS_DATA -P PROB_DATA] -a ATM_PARAM -x XS_PARAM -p PROB_PARAM -o OUT_FILE -t JSON_TABLE

# Options:
#   -h --help                            Help.
#   -a --atm_flux_parameters ATM_PARAM   JSON file with the atmospheric flux parameterisation.
#   -x --xs_parameters XS_PARAM    JSON file with the cross section parameterisation.  
#   -p --prob_param PROB_PARAM  JSON file with the parameterisation of the probability to get a 100TeV shower.
#   -A --atm_flux_data ATM_DATA   JSON file with the atmospheric flux parameterisation.
#   -X --xs_data XS_DATA    JSON file with the cross section parameterisation.  
#   -P --prob_data PROB_DATA  JSON file with the parameterisation of the probability to get a 100TeV shower.
#   -o --output_file OUT_FILE JSON file with the results.
#   -t --json_table JSON_TABLE     JSON formatted table with all the analysis parameters.
# """

from docopt import docopt
from fiesta import nuBy as nb
from fiesta import nuFlux as nf
from fiesta import nuXs as nx
from fiesta import tools as tls
from fiesta import table as tbl
import numpy as np
import json
from scipy.integrate import quad
import matplotlib.pyplot as plt


def integrand_a_bg(e, x1, x2, x3, x4, p1, p2, f1, f2):
    """
    Integrand corresponding to the product of the cross section, the flux, and the probability to produce a cascade between in a certain energy range

    Keyword arguments:
    e -- energy
    x1 -- cross section parameter a1
    x2 -- cross section parameter b1
    x3 -- cross section parameter a2
    x4 -- cross section parameter b2
    p1 -- proba parameter phi
    p2 -- proba parameter gamma
    f1 -- flux parameter phi
    f2 -- flux parameter gamma
    """
    return nx.dis_xs(np.log10(e), x1, x2, x3, x4)*nb.p_100TeV(e, p1, p2)*nf.atmospheric_flux(e, f1, f2)

def integrand_b_bg(e, x1, x2, x3, x4, f1, f2):
    """
    Integrand corresponding to the product of the cross section and the flux.

    Keyword arguments:
    e -- energy
    x1 -- cross section parameter a1
    x2 -- cross section parameter b1
    x3 -- cross section parameter a2
    x4 -- cross section parameter b2
    f1 -- flux parameter phi
    f2 -- flux parameter gamma
    """
    return nx.dis_xs(np.log10(e), x1, x2, x3, x4)*nf.atmospheric_flux(e, f1, f2)
    
def integrand_a_s(e, x1, x2, x3, x4, p1, p2, f1, f2, f3, f4):
    """
    Integrand corresponding to the product of the cross section, the flux, and the probability to produce a cascade between in a certain energy range

    Keyword arguments:
    e -- energy
    x1 -- cross section parameter a1
    x2 -- cross section parameter b1
    x3 -- cross section parameter a2
    x4 -- cross section parameter b2
    p1 -- proba parameter phi
    p2 -- proba parameter gamma
    f1 -- flux parameter phi
    f2 -- flux parameter gamma
    f3 -- flux parameter e0
    f4 -- flux parameter c0
    """
    return nx.dis_xs(np.log10(e), x1, x2, x3, x4)*nb.p_100TeV(e, p1, p2)*nf.astro_flux(e, f1, f2, f3, f4)/6.

def integrand_b_s(e, x1, x2, x3, x4, f1, f2, f3, f4):
    """
    Integrand corresponding to the product of the cross section, the flux, and the probability to produce a cascade between in a certain energy range

    Keyword arguments:
    e -- energy
    x1 -- cross section parameter a1
    x2 -- cross section parameter b1
    x3 -- cross section parameter a2
    x4 -- cross section parameter b2
    f1 -- flux parameter phi
    f2 -- flux parameter gamma
    f3 -- flux parameter e0
    f4 -- flux parameter c0
    """
    return nx.dis_xs(np.log10(e), x1, x2, x3, x4)*nf.astro_flux(e, f1, f2, f3, f4)/6.

def main():
    arguments = docopt(__doc__)

    # with open(arguments["--xs_parameters"], 'r') as xs_par_file:
    #     xs_parameters = json.load(xs_par_file)
    # xs_par_file.close()

    # with open(arguments["--atm_flux_parameters"], 'r') as atm_par_file:
    #     atm_parameters = json.load(atm_par_file)
    # atm_par_file.close()

    # with open(arguments["--prob_param"], 'r') as prob_par_file:
    #     prob_parameters = json.load(prob_par_file)
    # prob_par_file.close()

    t = tbl.table.from_json(arguments["--json_table"])

    d = t.get_table()

    
    astro_flx={'phi': 1.66, 'gamma': 2.53, 'e0': 100e3, 'c0': 3e-18}
    # xs_nc=xs_parameters['nc_nu']
    # p_100=prob_parameters['nu_mu_nc']
    # atm_nu_mu=atm_parameters['nu_mu']
    xs_nc=d['xs']['nu_nc']['data']
    p_100=d['p_cascade']['nu_mu_nc']['data']
    atm_nu_mu=d['flux']['atm']['nu_mu']['data']

    A_BG=quad(integrand_a_bg, 9e4, np.inf, args=(xs_nc['a1'],
                                                 xs_nc['b1'],
                                                 xs_nc['a2'],
                                                 xs_nc['b2'],
                                                 p_100['phi'],
                                                 p_100['gamma'],
                                                 atm_nu_mu['phi'],
                                                 atm_nu_mu['gamma']))
    
    A_SG=quad(integrand_a_s, 9e4, np.inf, args=(xs_nc['a1'],
                                                xs_nc['b1'],
                                                xs_nc['a2'],
                                                xs_nc['b2'],
                                                p_100['phi'],
                                                p_100['gamma'],
                                                astro_flx['phi'],
                                                astro_flx['gamma'],
                                                astro_flx['e0'],
                                                astro_flx['c0']))

    # xs_cc=xs_parameters['cc_nu']
    # atm_nu_e=atm_parameters['nu_e']

    xs_cc=d['xs']['nu_cc']['data']
    atm_nu_e=d['flux']['atm']['nu_e']['data']

    B_BG=quad(integrand_b_bg, 9e4, 1.1e5, args=(xs_cc['a1'],
                                                xs_cc['b1'],
                                                xs_cc['a2'],
                                                xs_cc['b2'],
                                                atm_nu_e['phi'],
                                                atm_nu_e['gamma']))

    B_SG=quad(integrand_b_s, 9e4, 1.1e5, args=(xs_cc['a1'],
                                               xs_cc['b1'],
                                               xs_cc['a2'],
                                               xs_cc['b2'],
                                               astro_flx['phi'],
                                               astro_flx['gamma'],
                                               astro_flx['e0'],
                                               astro_flx['c0']))
    
    print("A_SG= ", A_SG)
    print("B_SG= ", B_SG)
    print("A_BG= ", A_BG)
    print("B_BG= ", B_BG)
        
    p0=(A_SG[0]/(A_SG[0]+A_BG[0]))
    p1=(B_SG[0]/(B_SG[0]+B_BG[0]))

    print(p0,p1)
    
    p=(A_SG[0]+B_SG[0])/(A_SG[0]+B_SG[0]+A_BG[0]+B_BG[0])
    print(p)

    results={}
    results['I1 signal']=A_SG
    results['I2 signal']=B_SG
    results['I1 background']=A_BG
    results['I2 background']=B_BG
    results['probability']=p

    with open(arguments['--output_file'], "w") as outfile:
        json.dump(results, outfile)
    outfile.close()

    # control plots

    emin = 9e4
    emax = 1.1e5
    n = 1000
    step = (emax-emin)/n
    en = np.arange(emin,emax,step)

    f1,a1=plt.subplots()
    
    a1.plot(en,integrand_b_bg(en,xs_cc['a1'],
                              xs_cc['b1'],
                              xs_cc['a2'],
                              xs_cc['b2'],
                              atm_nu_e['phi'],
                              atm_nu_e['gamma']), color='darkorange', label=(r"$\phi _{atm}(\nu _{e})\cdot \sigma _{CC}$"))
    
    a1.plot(en,integrand_b_s(en,xs_cc['a1'],
                             xs_cc['b1'],
                             xs_cc['a2'],
                             xs_cc['b2'],
                             astro_flx['phi'],
                             astro_flx['gamma'],
                             astro_flx['e0'],
                             astro_flx['c0']), color='royalblue', label=(r"$\phi _{astro}(\nu _{e})\cdot \sigma _{CC}$"))
    a1.legend()
    a1.set_yscale("log")
    a1.set_xscale("log")
    a1.set_title("integrand equation 2")
    a1.grid()
    f2,a2=plt.subplots()

    if (arguments['--atm_flux_data']!=None):
        flux=nf.read_flux_file(arguments["--atm_flux_data"])
        
    a2.plot(flux["E"],flux['nu_e'],
            color='red',
            label=(r"$\phi _{atm}(\nu _{e})$(data)"))
    
    a2.plot(en,nf.atmospheric_flux(en, atm_nu_e['phi'], atm_nu_e['gamma']),
            color='darkorange',
            label=(r"$\phi _{atm}(\nu _{e})$"))
    
    a2.plot(en, nf.astro_flux(en, astro_flx['phi'], astro_flx['gamma'], astro_flx['e0'], astro_flx['c0'])/6.,
    color='royalblue',
    label=(r"$\phi _{astro}(\nu _{e})$"))

    a2.legend()
    a2.set_yscale("log")
    a2.set_xscale("log")
    a2.set_title("electron neutrino fluxes")
    a2.grid()
    emin = 9e4
    emax = 1e12
    
    n = 5000
    step = (emax-emin)/n
    en = np.arange(emin,emax,step)

    
    f3,a3=plt.subplots()

    a3.plot(en,integrand_a_bg(en,xs_cc['a1'],
                              xs_cc['b1'],
                              xs_cc['a2'],
                              xs_cc['b2'],
                              p_100['phi'],
                              p_100['gamma'],
                              atm_nu_mu['phi'],
                              atm_nu_mu['gamma']), color='darkorange', label=(r"$\phi _{atm}(\nu _{\mu})\cdot \sigma _{NC}\cdot p(90-110TeV)$"))

    a3.plot(en,integrand_a_s(en,xs_cc['a1'],
                             xs_cc['b1'],
                             xs_cc['a2'],
                             xs_cc['b2'],
                             p_100['phi'],
                             p_100['gamma'],
                             astro_flx['phi'],
                             astro_flx['gamma'],
                             astro_flx['e0'],
                             astro_flx['c0']), color='royalblue', label=(r"$\phi _{astro}(\nu _{\mu})\cdot \sigma _{NC}\cdot p(90-110TeV)$"))

    a3.legend()
    a3.set_yscale("log")
    a3.set_xscale("log")
    a3.set_title("integrand equation 1")
    a3.grid()
    plt.show()
    
if __name__== '__main__':
    main()
