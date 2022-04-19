import sys
import json
import logging
import os
import copy
from typing import Dict


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def clear_cell():
    return


def main():
    if len(sys.argv) < 2:
        logging.error('not enough arguments')
        return 1
    
    if not os.path.exists(sys.argv[1]):
        logging.error('file does not exist')
        return 1

    if not sys.argv[1].endswith('.ipynb'):
        logging.error('file is not a notebook')
        return 1

    # read json
    try:
        f_open = open(sys.argv[1], 'r')
        jupyter_json = json.load(f_open)
    except Exception as err:
        logging.error('error opening file, {}'.format(err))
        return 1
    
    f_open.close()
    cleared_jupyter_json = clear_jupyter_output(jupyter_json)

    print(jupyter_json)
    print(cleared_jupyter_json)

    if cleared_jupyter_json is not None:
        f_write = open(sys.argv[1], 'w')
        json.dump(cleared_jupyter_json, f_write)
    else:
        logging.error('could not process jupyter file')

    return 0


def clear_jupyter_output(jupyter_json: Dict, not_clear_signal='commit-output') -> Dict:
    """
    Clear cell outputs from a jupyter notebook.
    While remain cell outputs with 'cimmit-outpt' in source cell.
    """
    cleared_jupyter_json = copy.deepcopy(jupyter_json)
    if 'cells' in cleared_jupyter_json:
        for cell in cleared_jupyter_json['cells']:
            if 'outputs' in cell.keys() and 'source' in cell.keys():
                if len(cell['source']) > 1 and not_clear_signal in cell['source'][0]:
                    continue
                else:
                    cell['outputs'] = []
            else:
                return None
    else:
        return None
    return cleared_jupyter_json


if __name__ == "__main__":
    main()