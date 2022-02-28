"""
Usage: extractGSeaGenData.py -o OUTPUT_FILE -i INPUT_PATH

Options:
  -h --help                      Help.
  -o --output_file OUTPUT_FILE   Output file.
  -i --input_path INPUT_PATH     Input path.
"""

from docopt import docopt
from pathlib import Path
from fiesta import nuBy as nb
from fiesta import tools as tls
from os.path import exists
import glob, os
import h5py
import pickle as pkl
import numpy as np
import boost_histogram as bh

def main():
    arguments = docopt(__doc__)

    # define E bins
    logE_min = 2.0
    logE_max = 8.0
    N_e = 100
    step_e = (logE_max - logE_min)/N_e
    logE_bins = np.arange(logE_min,logE_max+step_e,step_e)
    E_bins = np.power(10,logE_bins)

    # define By bins
    logBy_min = -3.5
    logBy_max = 0
    N_logBy = 400
    step_logBy = (logBy_max - logBy_min)/N_logBy
    logBy_bins = np.arange(logBy_min,logBy_max+step_logBy,step_logBy)
    By_bins = np.power(10,logBy_bins)
    
    e_vs_by = bh.Histogram(
        bh.axis.Variable(E_bins),
        bh.axis.Variable(By_bins)
    )

    by_files=glob.glob(arguments['--input_path']+"*.hdf5")

    for file in by_files:
        h5 = h5py.File(file, "r")
        e_vs_by.fill(np.array(h5['e']), np.array(h5['by']))
        h5.close()

    with open(arguments['--output_file'], "wb") as f:
        pkl.dump(e_vs_by, f)
    
if __name__== '__main__':
    main()
