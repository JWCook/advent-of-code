"""https://adventofcode.com/2023/day/1"""
from loguru import logger

from .utils import Solution, read_input

digit_strs = {
    'zero': '0',
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}


def sum_line_1(line: str) -> int:
    digits = [c for c in line if c.isdigit()]
    return 0 if not digits else int(digits[0] + digits[-1])


def sum_line_2(line: str) -> int:
    digits = []
    for pos in range(len(line)):
        for s, i in digit_strs.items():
            if line[pos:].startswith(s):
                digits.append(i)
        if line[pos].isdigit():
            digits += line[pos]

    total = int(digits[0] + digits[-1])
    logger.debug(f'{line} -> {digits} -> {total}')
    return total


def solve(**kwargs) -> Solution:
    data = read_input(1, **kwargs)

    answer_1 = sum([sum_line_1(line) for line in data.splitlines()])
    logger.info(f'Part 1: {answer_1}')

    answer_2 = sum([sum_line_2(line) for line in data.splitlines()])
    logger.info(f'Part 2: {answer_2}')

    return answer_1, answer_2
