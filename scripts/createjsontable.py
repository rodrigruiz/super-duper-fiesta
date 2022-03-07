"""
Usage: createjsontable.py -o OUT_FILE

Options:
  -h --help                 Help.
  -o --output_file OUT_FILE JSON file with the results.
"""

from docopt import docopt
from fiesta import tools as tls
from pathlib import Path
import json

def main():
    arguments = docopt(__doc__)

    if (Path(arguments['--output_file']).is_file()):
        print("ERROR: Output file exists and won't be overwritten")
        exit(1)

    particles=["nu", "anu"]
    flavors  =["e", "mu", "tau"]
    channels =["cc", "nc"]

    # d={}

    # Flux:
    flux={}
    fm={}
    fm["units"]=None
    flux["metadata"]=fm

    astro={}
    astro["phi"]  =None
    astro["gamma"]=None
    astro["e0"]   =None
    astro["c0"]   =None

    flux["astro"] =astro

    atm={}
    for p in particles:
        for f in flavors:
            m={'emin': None, 'emax': None}
            d={'phi': None, 'gamma': None}
            atm[p+'_'+f]={'metadata': m, 'data': d}

    flux["atm"]=atm

    # Cross section:
    xs={}
    xm={'units': None}
    xs['metadata']=xm
    for p in particles:
        for c in channels:
            m={'emin': None, 'emax': None}
            d={'a1': None, 'a2': None, 'b1': None, 'b2': None}
            xs[p+'_'+c]={'metadata': m, 'data': d}

    # Probability Cascade
    prob={}
    for p in particles:
        for f in flavors:
            for c in channels:
                m={'emin': None, 'emax': None}
                d={'phi': None, 'gamma': None}
            prob[p+'_'+f+'_'+c]={'metadata': m, 'data': d}

    d={}
    d["xs"]=xs
    d["flux"]=flux
    d['p_cascade']=prob
    with open(arguments["--output_file"], 'w') as outfile:
        json.dump(d, outfile)
    outfile.close()

if __name__== '__main__':
    main()
