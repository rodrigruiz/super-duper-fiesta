"""
Usage: printflux.py -t TABLE

Options:
  -h --help                 Help.
  -t --table TABLE JSON file with the results.
"""

from docopt import docopt
from fiesta import table as tbl
import json

def main():
    arguments = docopt(__doc__)

    t = tbl.table.from_json(arguments["--table"])

    d = t.get_table()

    print(json.dumps(d['xs'], sort_keys=False, indent=4))

if __name__== '__main__':
    main()
