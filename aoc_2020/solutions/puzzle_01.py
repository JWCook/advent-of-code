from itertools import product
from logging import getLogger
from math import prod as multiply
from random import shuffle
from typing import Tuple

from . import Solution, read_input

logger = getLogger(__file__)


def get_target_addends(numbers, target_sum, num_addends=2) -> Tuple[int, ...]:
    """Get an arbitrary number of numbers from the specified list that add up to a specified sum"""
    if target_sum in numbers and 0 in numbers:
        return target_sum, 0

    # Get sets of numbers to search in different sorting orders; start with desc and asc order
    numbers = sorted([n for n in numbers if n < target_sum])
    number_sets = [numbers, numbers[::-1]]
    # Any additional sets will be in randomized order
    for _ in range(num_addends - 2):
        number_set = numbers.copy()
        shuffle(number_set)
        number_sets.append(number_set)

    logger.info(
        f'Searching {len(numbers)} numbers for {num_addends} numbers with a sum of {target_sum}'
    )
    n_checks = 0
    for combination in product(*number_sets):
        n_checks += 1
        if sum(combination) == target_sum:
            logger.info(f'Found addends {combination} in {n_checks} iterations')
            return combination

    logger.error('No solution found')
    return tuple([0] * num_addends)


def solve(**kwargs) -> Solution:
    data = read_input(1, **kwargs).splitlines()
    numbers = list(map(int, data))

    addends = get_target_addends(numbers, 2020, 2)
    answer_1 = multiply(addends)

    addends = get_target_addends(numbers, 2020, 3)
    answer_2 = multiply(addends)
    return answer_1, answer_2
