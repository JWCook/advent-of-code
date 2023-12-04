#!/usr/bin/env python3
# https://adventofcode.com/2022/day/12
import networkx as nx
from loguru import logger

from . import read_input

UNICODE_OFFSET = 96

HeightMap = list[list[int]]


def parse_map(data: str):
    heightmap = []
    start = None
    end = None

    for y, line in enumerate(data.splitlines()):
        heightmap_row = []
        for x, char in enumerate(line):
            if char == 'S':
                start = (x, y)
                height = 1
            elif char == 'E':
                end = (x, y)
                height = 26
            else:
                height = ord(char) - UNICODE_OFFSET
            heightmap_row.append(height)
        heightmap.append(heightmap_row)

    return heightmap, start, end


def format_map(heightmap: HeightMap, path=None):
    def format_point(x, y, i):
        return '**' if path and (x, y) in path else f'{i:>2}'

    return '\n'.join(
        [
            ' '.join([format_point(x, y, i) for x, i in enumerate(row)])
            for y, row in enumerate(heightmap)
        ]
    )


def build_graph(heightmap: HeightMap):
    # Add nodes
    graph = nx.Graph().to_directed()
    for x in range(len(heightmap[0])):
        for y in range(len(heightmap)):
            graph.add_node((x, y))

    # Add edges
    for x in range(len(heightmap[0])):
        for y in range(len(heightmap)):
            for n_x, n_y in get_neighbors(heightmap, x, y):
                graph.add_edge((x, y), (n_x, n_y))

    logger.debug(list(graph.nodes))
    logger.debug(list(graph.edges))
    return graph


def get_neighbors(heightmap: HeightMap, x: int, y: int):
    neighbors = []
    if x > 0 and (heightmap[y][x - 1] - heightmap[y][x]) <= 1:
        neighbors.append((x - 1, y))
    if x < len(heightmap[0]) - 1 and (heightmap[y][x + 1] - heightmap[y][x]) <= 1:
        neighbors.append((x + 1, y))
    if y > 0 and (heightmap[y - 1][x] - heightmap[y][x]) <= 1:
        neighbors.append((x, y - 1))
    if y < len(heightmap) - 1 and (heightmap[y + 1][x] - heightmap[y][x]) <= 1:
        neighbors.append((x, y + 1))
    return neighbors


def shortest_path(graph, start, end):
    return nx.shortest_path(graph, start, end)


def find_shortest_path(heightmap: HeightMap, start: int, end: int) -> int:
    graph = build_graph(heightmap)
    path = shortest_path(graph, start, end)
    logger.debug(path)
    logger.debug('\n' + format_map(heightmap))
    logger.info('\n' + format_map(heightmap, path))
    return len(path) - 1


def find_shortest_path_from_any_start(heightmap: HeightMap, end: int) -> int:
    starts = [
        (x, y)
        for x in range(len(heightmap[0]))
        for y in range(len(heightmap))
        if heightmap[y][x] == 1
    ]
    lengths = []

    for start in starts:
        graph = build_graph(heightmap)
        try:
            path = shortest_path(graph, start, end)
        except:
            pass
        lengths.append(len(path) - 1)

    return min(lengths)


if __name__ == '__main__':
    data = read_input(12)
    heightmap, start, end = parse_map(data)
    logger.info(f'Part 1: {find_shortest_path(heightmap, start, end)}')
    logger.info(f'Part 2: {find_shortest_path_from_any_start(heightmap, end)}')
