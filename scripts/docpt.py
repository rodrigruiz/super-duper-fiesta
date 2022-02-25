"""
Usage: docopt.py [-o OUTPUT_FILE] -f INPUT_FILE

Options:
  -h --help                                Help.
  -o --output_file OUTPUT_FILE             Output file. [type: str]
  -f --input_file INPUT_FILE               Input file.  [type: str]
"""
#from type_docopt import docopt
from docopt import docopt
from pathlib import Path

def main():
    arguments = docopt(__doc__)
    print(arguments)

    if (arguments['--output_file']==None):
        print("using default name for output file")
        arguments['--output_file']=Path(arguments['--input_file']).stem+'.rates.hdf5'
    print(arguments)
if __name__== '__main__':
    main()
