"""
Usage: test.py -i INPUT_FILE
Options:
  -h --help                   Help.
  -i --input_file INPUT_FILE  Input file.
"""

from docopt import docopt

arguments = docopt(__doc__)
print(arguments)
