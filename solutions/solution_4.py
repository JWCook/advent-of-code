#!/usr/bin/env python3
# https://adventofcode.com/2023/day/4
from loguru import logger

from . import read_input


def parse_card(line: str) -> int:
    card_sets = line.split(':')[1].split('|')
    want = {int(i) for i in card_sets[0].split(' ') if i}
    have = {int(i) for i in card_sets[1].split(' ') if i}
    return len(want & have)


def score(n_matches: int) -> int:
    if not n_matches:
        return 0

    score = 1
    for _ in range(n_matches - 1):
        score *= 2
    return score


if __name__ == '__main__':
    data = read_input(4)
    matches = [parse_card(line) for line in data.splitlines()]
    scores = [score(n) for n in matches]
    logger.info(f'Part 1: {sum(scores)}')
