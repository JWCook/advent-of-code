# https://adventofcode.com/2022/day/4
import re
from logging import getLogger
from typing import Iterator

from . import Solution, read_input

logger = getLogger(__name__)

IntRanges = tuple[set[int], set[int]]
LINE_PATTERN = re.compile(r'(\d+)\-(\d+),(\d+)-(\d+)')


def parse_ranges(data: str) -> Iterator[IntRanges]:
    for line in data.splitlines():
        ints = [int(i) for i in LINE_PATTERN.match(line).groups()]  # type: ignore
        yield set(range(ints[0], ints[1] + 1)), set(range(ints[2], ints[3] + 1))


def count_subsets(data: str) -> int:
    def is_subset(range_1, range_2) -> bool:
        return not range_1 - range_2 or not range_2 - range_1

    return sum(1 for range_1, range_2 in parse_ranges(data) if is_subset(range_1, range_2))


def count_overlaps(data: str) -> int:
    def has_overlap(range_1, range_2) -> bool:
        return bool(range_1 & range_2)

    return sum(1 for range_1, range_2 in parse_ranges(data) if has_overlap(range_1, range_2))


def solve(**kwargs) -> Solution:
    data = read_input(4, **kwargs)
    return (
        count_subsets(data),
        count_overlaps(data),
    )
