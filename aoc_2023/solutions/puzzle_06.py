"""https://adventofcode.com/2023/day/6"""
import math
from typing import Iterable

from aoc_utils import read_input

Race = tuple[int, int]


def parse_races(data: list[str]) -> Iterable[Race]:
    return zip(
        [int(t) for t in data[0].split()[1:]],
        [int(d) for d in data[1].split()[1:]],
        strict=True,
    )


def parse_single_race(data: list[str]) -> Race:
    return (
        int(''.join(data[0].split()[1:])),
        int(''.join(data[1].split()[1:])),
    )


def combined_ways_to_win(races: Iterable[Race]) -> int:
    return math.prod(ways_to_win(time, dist) for time, dist in races)


def ways_to_win(time: int, dist: int) -> int:
    def is_winnable(charge):
        return charge * (time - charge) > dist

    return sum(is_winnable(charge) for charge in range(1, time))


def solve(**kwargs):
    data = read_input(2023, 6, **kwargs).splitlines()
    answer_1 = combined_ways_to_win(parse_races(data))
    answer_2 = ways_to_win(*parse_single_race(data))
    return (answer_1, answer_2)
