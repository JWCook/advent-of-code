from importlib import import_module
from pkgutil import iter_modules
from types import ModuleType
from typing import Iterator

from solutions import INPUTS_DIR, SOLUTIONS_DIR


def read_input(day: int, test: bool = False) -> str:
    filename = f'input_{day}_test' if test else f'input_{day}'
    return (INPUTS_DIR / filename).read_text()


def get_solution_modules() -> Iterator[ModuleType]:
    """Get all modules in the solutions package"""
    for module_info in iter_modules([str(SOLUTIONS_DIR)]):
        if module_info.name.startswith('solution_'):
            yield import_module(f'solutions.{module_info.name}')
