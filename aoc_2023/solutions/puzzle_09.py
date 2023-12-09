"""https://adventofcode.com/2023/day/9"""
from loguru import logger

from aoc_utils import Solution, read_input


def parse(data: str) -> list[list[int]]:
    return [[int(num) for num in line.split()] for line in data.splitlines()]


def sequence_diff(history: list[int]) -> list[int]:
    return [history[i] - history[i - 1] for i in range(1, len(history))]


def extrapolate_history(history: list[int]) -> list[int]:
    logger.debug(f'History: {history}')
    sequences = [history]
    next_line = history
    while not all(i == 0 for i in next_line):
        next_line = sequence_diff(next_line)
        sequences.append(next_line)

    sequences.reverse()
    for i in range(1, len(sequences) - 1):
        sequences[i + 1].append(sequences[i + 1][-1] + sequences[i][-1])
        sequences[i + 1].insert(0, sequences[i + 1][0] - sequences[i][0])
        logger.debug(f'Sequence {i}: {sequences[i]}')

    logger.debug(f'Extrapolated: {sequences[-1]}')
    return sequences[-1]


def solve(**kwargs) -> Solution:
    data = read_input(2023, 9, **kwargs)
    extrapolated = [extrapolate_history(history) for history in parse(data)]

    answer_1 = sum(h[-1] for h in extrapolated)
    answer_2 = sum(h[0] for h in extrapolated)
    return (answer_1, answer_2)
