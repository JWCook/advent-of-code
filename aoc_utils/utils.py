import re
from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules
from sys import stderr
from types import ModuleType
from typing import Any, Iterator

from jinja2 import Template
from loguru import logger

Solution = tuple[Any, Any]
BASE_DIR = Path(__file__).parent.parent
PUZZLE_TEMPLATE = Path(__file__).parent / 'puzzle.py.jinja'
MODULE_PATTERN = re.compile(r'puzzle_(\d+)$')


def create_template(year: int, puzzle_id: int):
    """Create template files for a new puzzle"""
    # Make parent directories
    year_dir = BASE_DIR / f'aoc_{year}'
    inputs_dir = year_dir / 'inputs'
    inputs_dir.mkdir(parents=True, exist_ok=True)
    solutions_dir = year_dir / 'solutions'
    solutions_dir.mkdir(exist_ok=True)

    # Create empty input files
    input_file = inputs_dir / f'input_{puzzle_id:02d}'
    input_file.touch()
    input_test_file = inputs_dir / f'input_{puzzle_id:02d}_test'
    input_test_file.touch()

    # Create solution file from template
    puzzle_file = solutions_dir / f'puzzle_{puzzle_id:02d}.py'
    if not puzzle_file.exists():
        template = Template(PUZZLE_TEMPLATE.read_text())
        puzzle_file.write_text(template.render(year=year, day=puzzle_id))


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
