import re
from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules
from sys import stderr
from types import ModuleType
from typing import Any, Iterator

from jinja2 import Template
from loguru import logger
from requests import HTTPError
from requests.utils import default_user_agent
from requests_cache import CachedSession

Solution = tuple[Any, Any]

BASE_DIR = Path(__file__).parent.parent
PUZZLE_TEMPLATE = Path(__file__).parent / 'puzzle.py.jinja'
MODULE_PATTERN = re.compile(r'puzzle_(\d+)$')

INPUT_URL = 'https://adventofcode.com/{year}/day/{day}/input'
SESSION_FILE = BASE_DIR / '.session'


def create_template(year: int, puzzle_id: int):
    """Create template files for a new puzzle.
    If a session cookie is found, the input will be downloaded.
    """
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

    # Download input if possible
    if input_content := download_input(year, puzzle_id):
        input_file.write_text(input_content)

    # Create solution file from template
    puzzle_file = solutions_dir / f'puzzle_{puzzle_id:02d}.py'
    if puzzle_file.exists():
        logger.warning(f'File already exists: {puzzle_file}')
    else:
        template = Template(PUZZLE_TEMPLATE.read_text())
        puzzle_file.write_text(template.render(year=year, day=puzzle_id))


def download_input(year: int, puzzle_id: int) -> str:
    """Download input from AoC website"""
    if not SESSION_FILE.is_file():
        logger.warning(
            f'No session cookie found. Copy from your browser and save to {SESSION_FILE}'
        )
        return ''

    session = CachedSession('aoc.db', use_cache_dir=True)
    cookie = SESSION_FILE.read_text().strip().replace('session=', '')
    response = session.get(
        INPUT_URL.format(year=year, day=puzzle_id),
        headers={'User-Agent': default_user_agent() + ' github.com:JWCook'},
        cookies={'session': cookie},
    )

    try:
        response.raise_for_status()
    except HTTPError as e:
        logger.warning(f'Failed to download input for {year}/{puzzle_id}')
        logger.debug(e)
        return ''

    source = 'cached' if response.from_cache else 'downloaded'
    logger.info(f'Found input for {year}/{puzzle_id} ({source})')
    return response.text


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
