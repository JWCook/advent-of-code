#!/usr/bin/env python3
# https://adventofcode.com/2022/day/6
from loguru import logger

from . import read_input


def find_marker(data: str, marker_len: int) -> int:
    for i in range(len(data)):
        if len(set(data[i : i + marker_len])) == marker_len:
            return i + marker_len


if __name__ == '__main__':
    data = read_input(6)
    logger.info(f'Part 1: {find_marker(data, 4)}')
    logger.info(f'Part 2: {find_marker(data, 14)}')
