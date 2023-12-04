#!/usr/bin/env python
from time import time

import click
from loguru import logger
from rich import print
from rich_click import RichCommand

from aoc_utils import get_puzzle_modules, set_log_level


@click.command(cls=RichCommand)
@click.argument('puzzle_ids', nargs=-1, type=int)
@click.option('-t', '--test', is_flag=True, show_default=True, default=False, help='Use test input')
@click.option('-v', '--verbose', count=True, help='Increase logging verbosity')
@click.option('-y', '--year', type=int, default=2023, help='AoC year to run')
def run(puzzle_ids: tuple[int], test: bool, verbose: int, year: int):
    """Run the specified puzzles, or all puzzles if none are given."""
    set_log_level(verbose)
    solution_modules = dict(enumerate(get_puzzle_modules(year), start=1))
    puzzle_ids = puzzle_ids or list(solution_modules.keys())
    total_start_time = time()

    for puzzle_id in puzzle_ids:
        try:
            module = solution_modules[puzzle_id]
        except KeyError:
            print(f'[red]No puzzle found for id [white]{puzzle_id}')
            continue

        print(f'[blue]Running puzzle [white]{puzzle_id}')
        start_time = time()
        answer_1, answer_2 = module.solve(test=test)

        logger.info(f'Completed in {time() - start_time:.3f}s')
        print(f'  [green]⟫ [blue]Solution {puzzle_id}a: [white]{answer_1}')
        print(f'  [green]⟫ [blue]Solution {puzzle_id}b: [white]{answer_2}')

    logger.info(f'Completed {len(puzzle_ids)} puzzles in {time() - total_start_time:.3f}s')


if __name__ == '__main__':
    run()