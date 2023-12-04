import re
from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules
from sys import stderr
from types import ModuleType
from typing import Any, Iterator

from loguru import logger

Solution = tuple[Any, Any]
BASE_DIR = Path(__file__).parent.parent
MODULE_PATTERN = re.compile(r'puzzle_(\d+)$')


def get_puzzle_modules(year: int) -> Iterator[ModuleType]:
    """Get all modules in the solutions package"""
    solutions_dir = BASE_DIR / f'aoc_{year}' / 'solutions'
    for module_info in iter_modules([str(solutions_dir)]):
        if MODULE_PATTERN.match(module_info.name):
            yield import_module(f'aoc_{year}.solutions.{module_info.name}')


def read_input(puzzle_id: int, year: int, test: bool = False) -> str:
    inputs_dir = BASE_DIR / f'aoc_{year}' / 'inputs'
    filename = f'input_{puzzle_id:02d}'
    if test:
        filename += '_test'
    return (inputs_dir / filename).read_text()


def set_log_level(verbosity: int):
    """Set logging level based on CLI verbosity option"""
    logger.remove()
    match verbosity:
        case 0:
            logger.add(stderr, level='WARNING')
        case 1:
            logger.add(stderr, level='INFO')
        case _:
            logger.add(stderr, level='DEBUG')
