"""https://adventofcode.com/2021/day/2"""
from dataclasses import dataclass, field

from loguru import logger

from . import Solution, read_input


@dataclass
class Coords:
    x: int = field(default=0)
    y: int = field(default=0)
    aim: int = field(default=0)
    ortho: bool = field(default=True)

    def __post_init__(self):
        self.directions = {
            'up': lambda val: self._move_direct(y=val),
            'down': lambda val: self._move_direct(y=-1 * val),
            'forward': lambda val: self._move_direct(x=val),
        }

    def move(self, direction: str, distance: int):
        """Move based on direction string and distance"""
        func = self.directions[direction]
        func(distance)
        logger.debug(f'Moved {direction} {distance} to\t{self}')

    def _move_direct(self, x: int = 0, y: int = 0):
        """Move based on x and y values"""
        self.x += x
        if not self.ortho and y:
            self.aim += y
        elif not self.ortho and x:
            self.y += x * self.aim
        else:
            self.y += y

    def __str__(self):
        return f'({self.x}, {self.y}) | {self.aim}°'


def move_sub_1(directions: list[tuple[str, int]]) -> Coords:
    """Move based on direction string and distance"""
    pos = Coords()
    for direction, distance in directions:
        pos.move(direction, distance)
    logger.info(f'Final position: {pos}')
    return pos


def move_sub_2(directions: list[tuple[str, int]]) -> Coords:
    """Move based on direction string and distance, using aim"""
    pos = Coords(ortho=False)
    for direction, distance in directions:
        pos.move(direction, distance)
    logger.info(f'Final position: {pos}')
    return pos


def solve(**kwargs) -> Solution:
    data = read_input(2, **kwargs)
    directions = [(line.split()[0], int(line.split()[1])) for line in data.splitlines()]

    pos = move_sub_1(directions)
    answer_1 = abs(pos.x * pos.y)

    pos = move_sub_2(directions)
    answer_2 = abs(pos.x * pos.y)

    return (answer_1, answer_2)
