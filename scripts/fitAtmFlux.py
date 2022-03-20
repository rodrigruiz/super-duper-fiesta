"""
Usage: fitAtmFlux.py [-o OUTPUT_FILE] -i INPUT_FILE -e MIN_ENERGY -E MAX_ENERGY -f FLAVOR -t JSON_TABLE

Options:
  -h --help                      Help.
  -o --output_file OUTPUT_FILE   Output file.
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
from scipy.optimize import curve_fit
from os.path import exists
import json

def main():
    arguments = docopt(__doc__)

    if (not Path(arguments['--json_table']).is_file()):
        print("ERROR: JSON table does not exist")
        exit(1)

    if (arguments['--output_file']==None):
        arguments['--output_file']=Path(arguments['--input_file']).stem+'.json'

    emin=arguments["--e_min"]
    emax=arguments["--e_max"]    
    
    flux=nf.read_flux_file(arguments["--input_file"])

    i1=tls.find_nearest_index(flux["E"], float(emin))
    i2=tls.find_nearest_index(flux["E"], float(emax))

    a,b = curve_fit(nf.atmospheric_flux, flux["E"][i1:i2], flux[arguments["--flavor"]][i1:i2], maxfev=2000)



    if(Path(arguments['--output_file']).is_file()):
        print("output file exists. Updating it")
        with open(arguments["--output_file"], 'r') as json_file:
            d = json.load(json_file)
        json_file.close()

        d[arguments["--flavor"]]["phi"] = a[0]
        d[arguments["--flavor"]]["gamma"] = a[1]
        
        with open(arguments["--output_file"], 'w') as outfile:
            json.dump(d, outfile)
        outfile.close()
        
    else:
        print("output file does not exist. Creating it")
        d={}
        for key in ["nu_e", "nu_mu", "nu_e_bar", "nu_mu_bar"]:
            d[key]={"phi":0,"gamma":0}
            
        d[arguments["--flavor"]]["phi"] = a[0]
        d[arguments["--flavor"]]["gamma"] = a[1]
        
        with open(arguments["--output_file"], 'w') as outfile:
            json.dump(d, outfile)
        outfile.close()

    with open(arguments['--json_table'],'r') as json_file:
        table=json.load(json_file)
    json_file.close()

    table['flux']['atm'][arguments['--flavor']]['metadata']['emin']=emin
    table['flux']['atm'][arguments['--flavor']]['metadata']['emax']=emax
    table['flux']['atm'][arguments['--flavor']]['data']['phi']=a[0]
    table['flux']['atm'][arguments['--flavor']]['data']['gamma']=a[1]

    with open(arguments['--json_table'],'w') as json_file:
        table=json.dump(table, json_file)
    json_file.close()

if __name__== '__main__':
    main()
