# https://adventofcode.com/2022/day/6
from . import Solution, read_input


def find_marker(data: str, marker_len: int) -> int:
    for i in range(len(data)):
        if len(set(data[i : i + marker_len])) == marker_len:
            return i + marker_len
    return -1


def solve(**kwargs) -> Solution:
    data = read_input(6, **kwargs)
    return (
        find_marker(data, 4),
        find_marker(data, 14),
    )
