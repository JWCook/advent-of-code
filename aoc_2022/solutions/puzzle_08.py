#!/usr/bin/env python3
# https://adventofcode.com/2022/day/8
from loguru import logger

from . import read_input


def parse_trees(data: str) -> int:
    return [[int(x) for x in line.strip()] for line in data.splitlines()]


def count_visible_trees(tree_grid: list[list[int]]) -> int:
    grid_height = len(tree_grid)
    grid_width = len(tree_grid[0])

    def is_visible(x, y, tree_grid):
        tree_height = tree_grid[x][y]
        top = [tree_grid[x][i] for i in range(y + 1, grid_height)]
        bot = [tree_grid[x][i] for i in range(y)]
        left = [tree_grid[i][y] for i in range(x + 1, grid_width)]
        right = [tree_grid[i][y] for i in range(x)]
        return any([all([i < tree_height for i in lst]) for lst in [top, bot, left, right]])

    return sum(
        [1 for x in range(grid_width) for y in range(grid_height) if is_visible(x, y, tree_grid)]
    )


def max_scenic_score(tree_grid: list[list[int]]) -> int:
    grid_height = len(tree_grid)
    grid_width = len(tree_grid[0])

    def count_visible_trees_from(tree_height: int, lst: list[int]):
        visible_trees = 0
        for i in lst:
            visible_trees += 1
            if i >= tree_height:
                break
        return visible_trees

    def get_scenic_score(x, y, tree_grid):
        tree_height = tree_grid[x][y]
        top = [tree_grid[x][i] for i in range(y + 1, grid_height)]
        bot = [tree_grid[x][i] for i in reversed(range(y))]
        left = [tree_grid[i][y] for i in range(x + 1, grid_width)]
        right = [tree_grid[i][y] for i in reversed(range(x))]

        scenic_score = 1
        for lst in [top, bot, left, right]:
            scenic_score *= count_visible_trees_from(tree_height, lst)
        return scenic_score

    return max(
        [get_scenic_score(x, y, tree_grid) for x in range(grid_width) for y in range(grid_height)]
    )


if __name__ == '__main__':
    data = read_input(8)
    tree_grid = parse_trees(data)
    logger.info(f'Part 1: {count_visible_trees(tree_grid)}')
    logger.info(f'Part 2: {max_scenic_score(tree_grid)}')
