
"""
Usage: printjsontable.py -i INPUT_FILE

Options:
  -h --help                 Help.
  -i --input_file INPUT_FILE JSON file with the results.
"""

from docopt import docopt
from pathlib import Path
import json

def main():
    arguments = docopt(__doc__)

    # if (Path(arguments['--output_file']).is_file()):
    #     print("ERROR: Output file exists and won't be overwritten")
    #     exit(1)

    with open(arguments["--input_file"], 'r') as json_file:
        d=json.load(json_file)
    json_file.close()

    json_string=json.dumps(d, indent=2)
    print(json_string)

if __name__== '__main__':
    main()
