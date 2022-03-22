"""
Usage: fitXs.py -i INPUT_FILE -c CHANNEL -t JSON_TABLE

Options:
  -h --help                      Help.
  -i --input_file INPUT_FILE     Input file.
  -c --channel CHANNEL           Interaction channel (nu_cc, nu_nc, anu_cc, anu_nc).
  -t --json_table JSON_TABLE     JSON formatted table with all the analysis parameters.
"""

from docopt import docopt
from pathlib import Path
import numpy as np
from fiesta import nuXs as nx
from fiesta import tools as tls
from fiesta import table as tbl
from scipy.optimize import curve_fit
from os.path import exists
import json

def main():
    arguments = docopt(__doc__)

    xs=nx.read_xs_file(arguments["--input_file"])

    logEmin=5
    logEmax=12
    
    i1=tls.find_nearest_index(xs["log_E"], float(logEmin))
    i2=tls.find_nearest_index(xs["log_E"], float(logEmax))

    a,b = curve_fit(nx.dis_xs, xs["log_E"][i1:i2], xs[arguments["--channel"]][i1:i2], maxfev=2000)
    
    t = tbl.table.from_json(arguments["--json_table"])
    t.set_xs(arguments["--channel"], logEmin, logEmax, a[0], a[1], a[2], a[3])
    t.write(arguments["--json_table"])
        
if __name__== '__main__':
    main()
