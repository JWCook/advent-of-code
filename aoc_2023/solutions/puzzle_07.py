"""https://adventofcode.com/2023/day/7"""
from dataclasses import dataclass, field
from enum import Enum

from loguru import logger

from aoc_utils import Solution, read_input

CARDS = '23456789TJQKA'
CARDS_JOKER = 'J' + CARDS.replace('J', '')
HandType = Enum(
    'HandType',
    [
        'invalid',
        'high_card',
        'one_pair',
        'two_pair',
        'three_of_a_kind',
        'full_house',
        'four_of_a_kind',
        'five_of_a_kind',
    ],
)


@dataclass
class Hand:
    cards: str
    bet: int
    rank: int = field(default=0)
    joker: bool = field(default=False)
    type: HandType = field(default=HandType.invalid)

    @classmethod
    def from_str(cls, hand_str: str):
        cards, bet = hand_str.split()
        return cls(cards=cards, bet=int(bet))

    @property
    def sort_key(self) -> tuple[int, ...]:
        cards_lookup = CARDS_JOKER if self.joker else CARDS
        return (self.type.value, *[cards_lookup.index(c) for c in self.cards])

    @property
    def winnings(self) -> int:
        return self.bet * self.rank

    def classify_hand(self, joker: bool = False) -> 'Hand':
        self.joker = joker
        if self.joker and 'J' in self.cards:
            possible_types = [get_hand_type(self.cards.replace('J', card)) for card in CARDS]
            self.type = max(possible_types, key=lambda t: t.value)
        else:
            self.type = get_hand_type(self.cards)
        return self


def get_hand_type(cards: str) -> HandType:
    """Determine hand type based on the number of unique cards"""
    match len(set(cards)):
        case 1:
            return HandType.five_of_a_kind
        case 2:
            if any(cards.count(card) == 4 for card in cards):
                return HandType.four_of_a_kind
            else:
                return HandType.full_house
        case 3:
            if any(cards.count(card) == 3 for card in cards):
                return HandType.three_of_a_kind
            else:
                return HandType.two_pair
        case 4:
            return HandType.one_pair
        case _:
            return HandType.high_card


def get_winnings(hands: list[Hand], joker: bool = False) -> int:
    # Classify, sort, and rank
    hands = [hand.classify_hand(joker=joker) for hand in hands]
    hands = sorted(hands, key=lambda hand: hand.sort_key)
    for i, hand in enumerate(hands):
        hand.rank = i + 1

    # Get total winnings
    logger.debug('\n'.join(map(str, hands)))
    return sum(hand.winnings for hand in hands)


def solve(**kwargs) -> Solution:
    data = read_input(2023, 7, **kwargs)
    hands = [Hand.from_str(line) for line in data.splitlines()]
    return (
        get_winnings(hands, joker=False),
        get_winnings(hands, joker=True),
    )
