import sys
import json
import logging
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
        with open(jupyter_file, 'r') as f:
            jupyter_json = json.load(f)
        f.close()
    except Exception as err:
        logging.error('error opening file, {}'.format(err))
        exit(1)

    # write cleared json
    cleared_jupyter_json = clear_jupyter_output(jupyter_json, not_clear_signal)
    if cleared_jupyter_json is not None:
        try:
            with open(jupyter_file, 'w') as f:
                json.dump(cleared_jupyter_json, f)
            f.close()
        except Exception as err:
            logging.error('error writing file, {}'.format(err))
    else:
        logging.error('could not process jupyter file')
        exit(1)

    return 0


def clear_jupyter_output(jupyter_json: Dict, not_clear_signal='commit-output') -> Dict:
    """
    Clear cell outputs from a jupyter notebook.
    While remain cell outputs with 'cimmit-outpt' in source cell.
    """
    cleared_jupyter_json = copy.deepcopy(jupyter_json)
    if 'cells' not in cleared_jupyter_json:
        return None
    else:
        for cell in cleared_jupyter_json['cells']:
            if 'source' not in cell.keys():
                return None
            else:
                if len(cell['source']) > 1 and not_clear_signal in cell['source'][0]:
                    continue
                else:
                    cell['outputs'] = []
    return cleared_jupyter_json


if __name__ == "__main__":
    main()
