# https://adventofcode.com/2022/day/1
from typing import Iterator

from loguru import logger

from . import Solution, read_input


def get_elf_calories(data: str) -> Iterator[int]:
    input_iter = iter(data.splitlines())

    def next_elf_calories():
        calories = 0
        while line := next(input_iter).strip():
            calories += int(line)
        return calories

    while True:
        try:
            yield next_elf_calories()
        except StopIteration:
            break


def solve(**kwargs) -> Solution:
    data = read_input(1, **kwargs)
    elf_calories = sorted(get_elf_calories(data), reverse=True)
    answer_1 = elf_calories[0]
    answer_2 = sum(elf_calories[:3])
    logger.info(f'Part 1: {answer_1}')
    logger.info(f'Part 2: {answer_2}')
    return answer_1, answer_2
