"""
Usage: createjsontable.py -o OUT_FILE

Options:
  -h --help                 Help.
  -o --output_file OUT_FILE JSON file with the results.
"""

from docopt import docopt
from fiesta import table as tbl
from pathlib import Path

def main():
    arguments = docopt(__doc__)

    if (Path(arguments['--output_file']).is_file()):
        print("ERROR: Output file exists and won't be overwritten")
        exit(1)

    t = tbl.table() 
    t.write(arguments["--output_file"])

if __name__== '__main__':
    main()
