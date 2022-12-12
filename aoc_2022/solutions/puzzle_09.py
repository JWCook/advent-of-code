#!/usr/bin/env python3
# https://adventofcode.com/2022/day/9
from dataclasses import dataclass, field

from loguru import logger

from . import read_input


@dataclass
class Point:
    x: int = field(default=0)
    y: int = field(default=0)

    def move(self, direction: str):
        match direction:
            case 'U':
                self.y += 1
            case 'D':
                self.y -= 1
            case 'L':
                self.x -= 1
            case 'R':
                self.x += 1

    def __str__(self) -> str:
        return f'({self.x:>3}, {self.y:>3})'


def find_visited(data: str, n_segments: int) -> set[tuple[int, int]]:
    visited = {(0, 0)}
    rope_segments = [Point() for _ in range(n_segments)]

    for line in data.splitlines():
        direction, distance = line.split()
        logger.debug(f'[{len(visited):>4}] {direction} {distance}')

        for _ in range(int(distance)):
            rope_segments[0].move(direction)
            for i in range(1, n_segments):
                rope_segments[i] = move_segment(rope_segments[i - 1], rope_segments[i])
            visited.add((rope_segments[-1].x, rope_segments[-1].y))

    return visited


def move_segment(head: Point, tail: Point) -> Point:
    x_diff = abs(head.x - tail.x)
    y_diff = abs(head.y - tail.y)
    logger.debug(f'  {head} {tail}')
    if max(x_diff, y_diff) <= 1:
        return tail

    if x_diff > 0:
        tail.move('R' if head.x > tail.x else 'L')
    if y_diff > 0:
        tail.move('U' if head.y > tail.y else 'D')

    logger.debug(f'  Move:       {tail}')
    return tail


if __name__ == '__main__':
    data = read_input(9)
    logger.info(f'Part 1: {len(find_visited(data, 2))}')
    logger.info(f'Part 2: {len(find_visited(data, 10))}')
