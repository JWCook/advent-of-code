"""https://adventofcode.com/2021/day/3"""
from typing import Callable

from loguru import logger

from . import Solution, read_input


def most_common_bits(data: list[str]) -> str:
    """Return the most common bit in each position (column)"""

    def common_bit(pos: int) -> str:
        n_ones = sum([int(x[pos]) for x in data])
        return '1' if n_ones >= len(data) / 2 else '0'

    n_bits = len(data[0])
    return ''.join([common_bit(i) for i in range(n_bits)])


def get_power_consumption(data: list[str]) -> int:
    gamma = most_common_bits(data)
    epsilon = _invert_bits(gamma)
    gamma_int = _bin_to_int(gamma)
    epsilon_int = _bin_to_int(epsilon)

    logger.info(f'Gamma: {gamma} ({gamma_int}) | Epsilon: {epsilon} ({epsilon_int})')
    return gamma_int * epsilon_int


def get_life_support_rating(data: list[str]) -> int:
    o2 = get_o2_rating(data)
    co2 = get_co2_rating(data)
    o2_int = _bin_to_int(o2)
    co2_int = _bin_to_int(co2)

    logger.info(f'O2 generator rating: {o2} ({o2_int}) | CO2 scrubber rating: {co2} ({co2_int}))')
    return o2_int * co2_int


def get_o2_rating(data: list[str]) -> str:
    return filter_by_criteria(
        data,
        lambda data: most_common_bits(data),
    )


def get_co2_rating(data: list[str]) -> str:
    return filter_by_criteria(
        data,
        lambda data: _invert_bits(most_common_bits(data)),
    )


def filter_by_criteria(data: list[str], matches_criteria: Callable) -> str:
    """Incrementally eliminate numbers that don't meet the specified criteria for each bit position,
    until only one remains.
    """
    keep = data
    pos = 0
    while len(keep) > 1:
        mask = matches_criteria(keep)
        keep = [x for x in keep if x[pos] == mask[pos]]
        logger.debug(f'x[{pos}]={mask[pos]}: {len(keep)}')
        pos += 1

    return keep[0]


def _invert_bits(binary_str: str) -> str:
    return ''.join(['0' if x == '1' else '1' for x in binary_str])


def _bin_to_int(binary_str: str) -> int:
    return int(binary_str, 2)


def solve(**kwargs) -> Solution:
    data = read_input(3, **kwargs).splitlines()
    answer_1 = get_power_consumption(data)
    answer_2 = get_life_support_rating(data)
    return (answer_1, answer_2)
