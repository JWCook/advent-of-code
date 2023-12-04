from importlib import import_module
from pkgutil import iter_modules
from sys import stderr
from types import ModuleType
from typing import Any, Iterator

from loguru import logger

from solutions import INPUTS_DIR, SOLUTIONS_DIR

Solution = tuple[Any, Any]


def get_puzzle_modules() -> Iterator[ModuleType]:
    """Get all modules in the solutions package"""
    for module_info in iter_modules([str(SOLUTIONS_DIR)]):
        if module_info.name.startswith('puzzle_'):
            yield import_module(f'solutions.{module_info.name}')


def read_input(puzzle_id: int, test: bool = False) -> str:
    filename = f'input_{puzzle_id}_test' if test else f'input_{puzzle_id}'
    return (INPUTS_DIR / filename).read_text()


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
