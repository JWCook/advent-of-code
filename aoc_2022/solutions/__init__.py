from pathlib import Path
from sys import stderr

from loguru import logger

# Comment out these lines for debug logs
logger.remove()
logger.add(stderr, level='INFO')

INPUTS_DIR = Path(__file__).parent.parent / 'inputs'
SOLUTIONS_DIR = Path(__file__).parent.parent / 'solutions'


def read_input(day: int) -> str:
    with open(INPUTS_DIR / f'input_{day}') as f:
        return f.read()
