"""https://adventofcode.com/2023/day/10"""
from loguru import logger

from aoc_utils import Solution, read_input

Coords = tuple[int, int]

PIPE_CHARS = {
    'L': '└',
    'J': '┘',
    '7': '┐',
    'F': '┌',
    'S': '╋',
}
CONNECTS_N = '└┘|╋'
CONNECTS_S = '┌┐|╋'
CONNECTS_E = '└┌0-╋'
CONNECTS_W = '┘┐-╋'
DIRECTIONS = {
    CONNECTS_N: (CONNECTS_S, 0, -1),
    CONNECTS_S: (CONNECTS_N, 0, 1),
    CONNECTS_E: (CONNECTS_W, 1, 0),
    CONNECTS_W: (CONNECTS_E, -1, 0),
}


def parse_grid(data: str) -> list[str]:
    return [line.translate(str.maketrans(PIPE_CHARS)) for line in data.splitlines()]  # type: ignore


def find_start(grid: list[str]) -> Coords:
    for i, row in enumerate(grid):
        if '╋' in row:
            return (row.index('╋'), i)
    raise ValueError('No start found')


def find_next(grid, x, y, prev_x, prev_y) -> Coords:
    """Find the next pipe in the path"""
    char = grid[y][x]
    logger.debug(f'Current: {char}({x}, {y}) Prev: {grid[prev_y][prev_x]}({prev_x}, {prev_y})')
    for char_set, (valid_pipes, offset_x, offset_y) in DIRECTIONS.items():
        next_x = x + offset_x
        next_y = y + offset_y
        # fmt: off
        if (
            char in char_set                          # This pipe points in this direction
            and 0 <= next_x < len(grid[0])            # in bounds (x)
            and 0 <= next_y < len(grid)               # in bounds (y)
            and (next_x, next_y) != (prev_x, prev_y)  # not the previous pipe
            and grid[next_y][next_x] in valid_pipes   # next pipe is connected
        ):
            logger.debug(f'  Found next pipe at {next_x}, {next_y} ({grid[next_y][next_x]})')
            return next_x, next_y


def find_loop(grid: list[str]) -> list[Coords]:
    """Starting at the S/╋, find a loop in the grid as a list of coordinates"""
    start = find_start(grid)
    next_pos = find_next(grid, *start, *start)
    path = [start, next_pos]

    while (next_pos := find_next(grid, *next_pos, *path[-2])) != start:
        path.append(next_pos)

    logger.debug('\nPath:\n' + '\n'.join([f'{x}, {y}: {grid[y][x]}' for x, y in path]))
    return path


def solve(**kwargs) -> Solution:
    data = read_input(2023, 10, **kwargs)
    grid = parse_grid(data)
    logger.info('\n'.join(grid))

    path = find_loop(grid)
    answer_1 = int((len(path) - 1) / 2)
    return (answer_1, None)
