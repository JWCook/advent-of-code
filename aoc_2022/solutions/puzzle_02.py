#!/usr/bin/env python3
# https://adventofcode.com/2022/day/2
from dataclasses import dataclass, field
from enum import Enum

from loguru import logger

from . import read_input


class Shape(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    @classmethod
    def from_char(cls, char: str) -> 'Shape':
        return SHAPE_CODES[char]


class Result(Enum):
    LOSE = 0
    DRAW = 3
    WIN = 6

    @classmethod
    def from_char(cls, char: str) -> 'Result':
        return RESULT_CODES[char]


SHAPE_CODES = {
    'A': Shape.ROCK,
    'B': Shape.PAPER,
    'C': Shape.SCISSORS,
    'X': Shape.ROCK,
    'Y': Shape.PAPER,
    'Z': Shape.SCISSORS,
}

RESULT_CODES = {
    'X': Result.LOSE,
    'Y': Result.DRAW,
    'Z': Result.WIN,
}

WIN_CONDITIONS = {
    Shape.ROCK: Shape.SCISSORS,
    Shape.PAPER: Shape.ROCK,
    Shape.SCISSORS: Shape.PAPER,
}
LOSE_CONDITIONS = {v: k for k, v in WIN_CONDITIONS.items()}


@dataclass
class Round:
    opponent_shape: Shape = field()
    player_shape: Shape = field(default=None)
    result: Result = field(default=None)

    @classmethod
    def parse(cls, line: str, by_result: bool = False) -> 'Round':
        return cls._parse_by_result(line) if by_result else cls._parse_by_player_shape(line)

    @classmethod
    def _parse_by_player_shape(cls, line: str) -> 'Round':
        """
        Column 1: Opponent's shape
        Column 2: Player's shape
        """
        opponent_code, player_code = line.strip().split()
        return cls(
            opponent_shape=Shape.from_char(opponent_code),
            player_shape=Shape.from_char(player_code),
        )

    @classmethod
    def _parse_by_result(cls, line: str) -> 'Round':
        """
        Column 1: Opponent's shape
        Column 2: Result of round
        """
        opponent_code, result_code = line.strip().split()
        return cls(
            opponent_shape=Shape.from_char(opponent_code),
            result=Result.from_char(result_code),
        )

    def get_score(self) -> int:
        if not self.result:
            self.result = self._get_result()
        if not self.player_shape:
            self.player_shape = self._get_player_shape()
        logger.debug(str(self))
        return self.player_shape.value + self.result.value

    def _get_result(self) -> Result:
        """Given an opponent's shape and a player's shape, determine the result"""
        if self.opponent_shape == self.player_shape:
            return Result.DRAW
        elif WIN_CONDITIONS[self.player_shape] == self.opponent_shape:
            return Result.WIN
        else:
            return Result.LOSE

    def _get_player_shape(self) -> Shape:
        """Given an opponent's shape and a result, determine the player's shape"""
        if self.result == Result.DRAW:
            return self.opponent_shape
        elif self.result == Result.WIN:
            return LOSE_CONDITIONS[self.opponent_shape]
        else:
            return WIN_CONDITIONS[self.opponent_shape]

    def __str__(self):
        return (
            f'Opponent: {self.opponent_shape.name} | Player: {self.player_shape.name} | '
            f'Result: {self.result.name}'
        )


def tally_scores(data: str, by_result: bool) -> int:
    return sum(Round.parse(line, by_result=by_result).get_score() for line in data.splitlines())


def main():
    data = read_input(2)
    logger.info(f'Part 1: {tally_scores(data, by_result=False)}')
    logger.info(f'Part 2: {tally_scores(data, by_result=True)}')


if __name__ == '__main__':
    main()
