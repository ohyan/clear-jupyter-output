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
    with open(jupyter_file, 'r') as f_reader:
        jupyter_json = json.load(f_reader)
    f_reader.close()

    cleared_jupyter_json = clear_jupyter_output(jupyter_json, not_clear_signal)

    with open(jupyter_file, 'w') as f_writer:
        json.dump(cleared_jupyter_json, f_writer)
    return 0


def clear_jupyter_output(jupyter_json: Dict, not_clear_signal='commit-output') -> Dict:
    """
    Clear cell outputs from a jupyter notebook.
    While remain cell outputs with 'cimmit-outpt' in source cell.
    """
    cleared_jupyter_json = copy.deepcopy(jupyter_json)
    for cell in cleared_jupyter_json['cells']:
        if not_clear_signal in cell['source'][0]:
            # not clear cell output when not_clear_signal is in the cell
            continue
        else:
            cell['outputs'] = []
    return cleared_jupyter_json


if __name__ == "__main__":
    main()
