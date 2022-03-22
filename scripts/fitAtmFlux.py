"""
Usage: fitAtmFlux.py -i INPUT_FILE -e MIN_ENERGY -E MAX_ENERGY -f FLAVOR -t JSON_TABLE

Options:
  -h --help                      Help.
  -i --input_file INPUT_FILE     Input file.
  -e --e_min MIN_ENERGY          Minimum energy.
  -E --e_max MAX_ENERGY          Maximum energy.
  -f --flavor FLAVOR             Neutrino flavor(nu_e, nu_mu, anu_e, anu_mu).
  -t --json_table JSON_TABLE     JSON formatted table with all the analysis parameters.
"""

from docopt import docopt
from pathlib import Path
from fiesta import nuFlux as nf
from fiesta import tools as tls
from fiesta import table as tbl
from scipy.optimize import curve_fit
from os.path import exists
import json

def main():
    arguments = docopt(__doc__)

    if (not Path(arguments['--json_table']).is_file()):
        print("ERROR: JSON table does not exist")
        exit(1)

    emin=arguments["--e_min"]
    emax=arguments["--e_max"]    
    
    flux=nf.read_flux_file(arguments["--input_file"])

    i1=tls.find_nearest_index(flux["E"], float(emin))
    i2=tls.find_nearest_index(flux["E"], float(emax))

    a,b = curve_fit(nf.atmospheric_flux, flux["E"][i1:i2], flux[arguments["--flavor"]][i1:i2], maxfev=2000)
        
    t = tbl.table.from_json(arguments["--json_table"])
    t.set_atm_flux(arguments['--flavor'], emin, emax, a[0], a[1])    
    t.write(arguments["--json_table"])

if __name__== '__main__':
    main()
