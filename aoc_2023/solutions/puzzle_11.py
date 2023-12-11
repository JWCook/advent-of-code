"""https://adventofcode.com/2023/day/11"""
from itertools import combinations
from typing import Iterator

from loguru import logger

from aoc_utils import Solution, read_input

Coords = tuple[int, int]
EXPANSION_CHAR = '✺'


def get_galaxy_coords(map: list[str]) -> Iterator[Coords]:
    for y, row in enumerate(map):
        for x, col in enumerate(row):
            if col == '#':
                yield (x, y)


def expand_map(map: list[str]):
    # find any columns and rows that don't contain '#', and add a new column after each one
    new_map = []
    for i, row in enumerate(map):
        new_map.append(row)
        if '#' not in row:
            logger.debug(f'Found empty row: {i}')
            new_map.append(row)

    for i in reversed(range(len(map[0]))):
        if '#' not in [row[i] for row in new_map]:
            logger.debug(f'Found empty column: {i}')
            for j in range(len(new_map)):
                new_map[j] = new_map[j][:i] + '.' + new_map[j][i:]

    logger.debug('\n' + '\n'.join(new_map))
    return new_map


def get_all_shortest_paths(data: list[str]):
    map = expand_map(data)
    coords = get_galaxy_coords(map)
    for (x_1, y_1), (x_2, y_2) in combinations(coords, 2):
        yield abs(x_1 - x_2) + abs(y_1 - y_2)


def expand_map_2(map: list[str]):
    # find any rows that only contain '.'
    insert_row = EXPANSION_CHAR * len(map[0])
    new_map = []
    for i, row in enumerate(map):
        if '#' not in row:
            logger.debug(f'Found empty row: {i}')
            new_map.append(insert_row)
        else:
            new_map.append(row)

    # find any columns that don't contain '#', and add a new column after each one
    for i in reversed(range(len(map[0]))):
        if '#' not in [row[i] for row in new_map]:
            logger.debug(f'Found empty column: {i}')
            for j in range(len(new_map)):
                new_map[j] = new_map[j][:i] + EXPANSION_CHAR + new_map[j][i + 1 :]

    logger.debug('\n' + '\n'.join(new_map))
    return new_map


def shortest_path_2(map, x_1, y_1, x_2, y_2) -> int:
    """Navigate from (x_1, y_1) to (x_2, y_2), using only horizontal and vertical moves.
    'EXPANSION_CHAR' represents a distance of 1000000.
    """
    path_length = 0
    (cur_x, cur_y) = (x_1, y_1)
    while (cur_x, cur_y) != (x_2, y_2):
        if cur_x < x_2:
            (cur_x, cur_y) = (cur_x + 1, cur_y)
        elif cur_x > x_2:
            (cur_x, cur_y) = (cur_x - 1, cur_y)
        elif cur_y < y_2:
            (cur_x, cur_y) = (cur_x, cur_y + 1)
        elif cur_y > y_2:
            (cur_x, cur_y) = (cur_x, cur_y - 1)

        if map[cur_y][cur_x] == EXPANSION_CHAR:
            path_length += 1000000
        else:
            path_length += 1
    return path_length


def get_all_shortest_paths_2(data: list[str]):
    map = expand_map_2(data)
    coords = get_galaxy_coords(map)
    for pos_1, pos_2 in combinations(coords, 2):
        yield shortest_path_2(map, *pos_1, *pos_2)


def solve(**kwargs) -> Solution:
    data = read_input(2023, 11, **kwargs).splitlines()

    paths = get_all_shortest_paths(data)
    answer_1 = sum(paths)

    paths = get_all_shortest_paths_2(data)
    answer_2 = sum(paths)

    return (answer_1, answer_2)
