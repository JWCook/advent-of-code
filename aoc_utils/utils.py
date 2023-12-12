"""Misc utilitiy functions that don't fit elsewhere"""
import re
from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules
from sys import stderr
from types import ModuleType
from typing import Any, Iterator

from loguru import logger

BASE_DIR = Path(__file__).parent.parent
LOG_FORMAT = '<g>{time:HH:mm:ss}</> | <lvl>{level: <8}</>| <cyan>{module}</> | {message}'
MODULE_PATTERN = re.compile(r'puzzle_(\d+)$')

ModuleMap = dict[int, ModuleType]
Solution = tuple[Any, Any]


def get_puzzle_modules(year: int) -> Iterator[ModuleType]:
    """Get all modules in the solutions package"""
    solutions_dir = BASE_DIR / f'aoc_{year}' / 'solutions'
    for module_info in iter_modules([str(solutions_dir)]):
        if MODULE_PATTERN.match(module_info.name):
            yield import_module(f'aoc_{year}.solutions.{module_info.name}')


def set_log_level(verbose: int):
    """Set logging level based on CLI verbose option"""
    logger.remove()
    level = ''
    match verbose:
        case 0:
            level = 'WARNING'
        case 1:
            level = 'INFO'
        case _:
            level = 'DEBUG'
    logger.add(stderr, format=LOG_FORMAT, level=level)
