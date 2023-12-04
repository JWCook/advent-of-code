from time import time

import click
from loguru import logger
from rich import print
from rich_click import RichCommand

from solutions.utils import get_solution_modules, set_log_level


@click.command(cls=RichCommand)
@click.argument('solution_ids', nargs=-1, type=int)
@click.option('-t', '--test', is_flag=True, show_default=True, default=False, help='Use test input')
@click.option('-v', '--verbose', count=True, help='Increase logging verbosity')
def run(solution_ids: tuple[int], test: bool, verbose: int):
    """Run the specified solution numbers, or all solutions if none are given."""
    set_log_level(verbose)
    solution_modules = {i: m for i, m in enumerate(get_solution_modules(), start=1)}
    solution_ids = solution_ids or list(solution_modules.keys())

    for solution_id in solution_ids:
        try:
            module = solution_modules[solution_id]
        except KeyError:
            print(f'[red]No solution found for id [white]{solution_id}')
            continue

        print(f'[blue]Running solution {solution_id}')
        start_time = time()
        answer_1, answer_2 = module.solve(test=test)

        logger.info(f'Completed in {time() - start_time:.3f}s')
        print(f'  [green]⟫ [blue]Solution {solution_id}a: [white]{answer_1}')
        print(f'  [green]⟫ [blue]Solution {solution_id}b: [white]{answer_2}')


if __name__ == '__main__':
    run()
