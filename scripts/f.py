"""
Usage: f.py
Options:
  -h --help                              Help.
"""

from docopt import docopt
from fiesta import nuFlux as nf

def main():
    
    arguments = docopt(__doc__)
    print(arguments)
    # data = {}
    
    # for key in arguments:
    #     data[key.replace("-", "")] = arguments[key]
    # print(data)
    
    # if (data["output_file"]==None):
    #     data["output_file"]=Path(arguments['--input_file']).stem+'.fit.json'

    # flux=nf.read_flux_file(data["input_file"])
    # print(flux["nu_e"])

if __name__ == "__main__":
    main()