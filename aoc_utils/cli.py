#!/usr/bin/env python
from time import time

import click
from loguru import logger
from rich import print
from rich_click import RichCommand

from aoc_utils import create_template, get_puzzle_modules, set_log_level


@click.command(cls=RichCommand)
@click.argument('puzzle_ids', nargs=-1, type=int)
@click.option('-t', '--test', is_flag=True, show_default=True, default=False, help='Use test input')
@click.option('-y', '--year', type=int, default=2023, show_default=True, help='AoC year to run')
@click.option('-c', '--create', is_flag=True, help='Create a template for a new puzzle')
@click.option('-v', '--verbose', count=True, help='Increase logging verbosity')
def run(puzzle_ids: tuple[int], test: bool, year: int, create: bool, verbose: int):
    """Run the specified puzzles, or all puzzles if none are given."""
    set_log_level(verbose)
    if create:
        create_templates(puzzle_ids, year)
        return

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


def create_templates(puzzle_ids: tuple[int], year: int):
    if not puzzle_ids:
        print('[red]No puzzle IDs specified')
        return

    for puzzle_id in puzzle_ids:
        create_template(year, puzzle_id)

    print(
        f'[blue]Created files for puzzle(s) [white]{year}.' + ",".join([str(i) for i in puzzle_ids])
    )


if __name__ == '__main__':
    run()
