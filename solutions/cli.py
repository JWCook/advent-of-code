import click
from rich import print
from rich_click import RichCommand
from solutions.utils import get_solution_modules


@click.command(cls=RichCommand)
@click.argument('solution_ids', nargs=-1, type=int)
def run(solution_ids: tuple[int]):
    solution_modules = {i: m for i, m in enumerate(get_solution_modules(), start=1)}
    solution_ids = solution_ids or list(solution_modules.keys())

    for solution_id in solution_ids:
        try:
            module = solution_modules[solution_id]
        except KeyError:
            print(f'[red]No solution found for id [white]{solution_id}')
            continue

        print(f'[blue]Running solution [white]{solution_id}')
        module.solve()


if __name__ == '__main__':
    run()
