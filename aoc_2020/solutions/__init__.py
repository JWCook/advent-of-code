import logging
from os.path import abspath, dirname, join

INPUTS_DIR = join(abspath(dirname(dirname(__file__))), 'inputs')
logging.basicConfig(level='INFO')


def get_input_data(day: int, split=True):
    with open(join(INPUTS_DIR, f'input_{day}')) as f:
        contents = f.read()
    return contents.splitlines() if split else contents
