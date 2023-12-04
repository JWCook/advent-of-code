"""https://adventofcode.com/2021/day/1"""
from loguru import logger

from . import Solution, read_input


def get_increased_readings(readings: list[int]) -> list[bool]:
    increased = [False]
    increased += [readings[i] > readings[i - 1] for i in range(1, len(readings))]
    return increased


def get_sliding_windows(readings: list[int]) -> list[int]:
    windows = [sum(readings[i : i + 3]) for i in range(len(readings) - 2)]
    return windows


def solve(**kwargs) -> Solution:
    data = read_input(1, **kwargs)
    readings = [int(line.strip()) for line in data.splitlines()]

    increased = get_increased_readings(readings)
    answer_1 = sum(increased)
    summary = [f'{readings[i]}: {increased[i]}' for i in range(len(readings) - 1)]
    logger.debug('\n'.join(summary))

    windows = get_sliding_windows(readings)
    increased = get_increased_readings(windows)
    answer_2 = sum(increased)

    return (answer_1, answer_2)
