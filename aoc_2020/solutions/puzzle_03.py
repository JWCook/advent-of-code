#!/usr/bin/env python3
from logging import getLogger
from math import prod as multiply

from solutions import get_input_data

logger = getLogger(__file__)

SLOPE_INCREMENTS = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2),
]


def main():
    input_data = get_input_data(3)
    n_trees = count_trees_in_path(input_data)
    logger.info(f'Solution 3a: {n_trees}')

    n_trees_list = [count_trees_in_path(input_data, x, y) for x, y in SLOPE_INCREMENTS]
    n_trees_product = multiply(n_trees_list)
    logger.info(f'Solution 3b: {n_trees_product}')


def count_trees_in_path(input_data, x_increment=3, y_increment=1):
    """'.' represents an empty space, '#' represents a tree"""
    height = len(input_data)
    width = len(input_data[0])
    x_index = 0
    y_index = 0
    path_chars = ''
    logger.info(
        f'Counting trees encountered in a map {height} spaces high and '
        f'infinite width; {width} spaces repeating; Slope: ({x_increment}, {y_increment})'
    )

    for i in range(height):
        # Pattern repeats along X axis, so 'wrap' X index to equivalent list index
        wrapped_x_index = x_index % width
        logger.debug('Indices:', y_index, x_index, wrapped_x_index)
        path_chars += input_data[y_index][wrapped_x_index]

        # Move three spaces right, one space down
        x_index += x_increment
        y_index += y_increment
        if y_index >= height:
            break

    return path_chars.count('#')


if __name__ == '__main__':
    main()
