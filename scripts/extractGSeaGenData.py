"""
Usage: extractGSeaGenData.py -o OUTPUT_PATH -i INPUT_PATH

Options:
  -h --help                      Help.
  -o --output_path OUTPUT_PATH   Output path.
  -i --input_path INPUT_PATH     Input path.
"""

from docopt import docopt
from pathlib import Path
from fiesta import nuBy as nb
from fiesta import tools as tls
from os.path import exists
import glob, os
import h5py

def main():
    arguments = docopt(__doc__)

    gSeaGen_files=glob.glob(arguments['--input_path']+"*.root")

    for file in gSeaGen_files:
        output_file = os.path.join(arguments['--output_path'], Path(file).stem+'.hdf5')
        data = nb.extract_data(file)
        h5 = h5py.File(output_file, "w")
        for key, value in data.items():
            h5.create_dataset(str(key), data=value)
        h5.close()
        
if __name__== '__main__':
    main()
