import pandas as pd
import seaborn as sns

from . import SOLUTIONS_DIR, read_input
from .puzzle_09 import find_visited

sns.set_theme(style="darkgrid")


def plot_visited(data: str, n_segments: int):
    visited = find_visited(data, n_segments)
    df = pd.DataFrame.from_records(list(visited), columns=['x', 'y'])
    plot = sns.scatterplot(data=df, x='x', y='y')
    plot.get_figure().savefig(SOLUTIONS_DIR / 'problem_9.png')


if __name__ == '__main__':
    data = read_input(9)
    plot_visited(data, 2)
    plot_visited(data, 10)
