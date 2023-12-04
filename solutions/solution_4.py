#!/usr/bin/env python
# https://adventofcode.com/2023/day/4
from dataclasses import dataclass, field

from loguru import logger

from solutions.utils import read_input


@dataclass
class Card:
    idx: int
    n_matches: int
    n_copies: int = field(default=1)

    @classmethod
    def parse(cls, idx: int, line: str) -> 'Card':
        card_sets = line.split(':')[1].split('|')
        want = {int(i) for i in card_sets[0].split(' ') if i}
        have = {int(i) for i in card_sets[1].split(' ') if i}
        n_matches = len(want & have)
        return cls(idx, n_matches)

    def score(self) -> int:
        if not self.n_matches:
            return 0

        score = 1
        for _ in range(self.n_matches - 1):
            score *= 2
        return score


def add_copies(cards: list[Card]):
    for i, card in enumerate(cards):
        # For each copy of this card, add copies of the next n_matches cards below this one
        for _ in range(card.n_copies):
            n_available = min(len(cards) - i, card.n_matches)
            for j in range(n_available):
                cards[i + j + 1].n_copies += 1

    logger.debug('\n'.join([str(x) for x in cards]))
    return cards


def solve():
    data = read_input('4')
    cards = [Card.parse(i, line) for i, line in enumerate(data.splitlines())]

    total_score = sum([card.score() for card in cards])
    logger.info(f'Part 1: {total_score}')

    cards = add_copies(cards)
    total_cards = sum([card.n_copies for card in cards])
    logger.info(f'Part 2: {total_cards}')
