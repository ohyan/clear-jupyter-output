import sys
import json
import logging
import os
import copy
from typing import Dict
import click


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


@click.command()
@click.option('--jupyter_file', help='jupyter notebook neet to be cleared output')
@click.option('--not_clear_signal', help='not clear cell signal', default='commit-output')
def main(jupyter_file, not_clear_signal):  
    # read json
    try:
        f_open = open(jupyter_file, 'r')
        jupyter_json = json.load(f_open)
    except Exception as err:
        logging.error('error opening file, {}'.format(err))
        return 1
    f_open.close()

    # write cleared json
    cleared_jupyter_json = clear_jupyter_output(jupyter_json, not_clear_signal)
    if cleared_jupyter_json is not None:
        f_write = open(jupyter_file, 'w')
        json.dump(cleared_jupyter_json, f_write)
    else:
        logging.error('could not process jupyter file')
        return 1

    return 0


def clear_jupyter_output(jupyter_json: Dict, not_clear_signal='commit-output') -> Dict:
    """
    Clear cell outputs from a jupyter notebook.
    While remain cell outputs with 'cimmit-outpt' in source cell.
    """
    cleared_jupyter_json = copy.deepcopy(jupyter_json)
    for cell in cleared_jupyter_json['cells']:
        if len(cell['source']) > 1 and not_clear_signal in cell['source'][0]:
            continue
        else:
            cell['outputs'] = []
    return cleared_jupyter_json


if __name__ == "__main__":
    main()
