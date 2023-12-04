"""https://adventofcode.com/2023/day/2"""
from dataclasses import dataclass

from loguru import logger

from . import Solution, read_input


@dataclass
class GameRecord:
    id: int
    max_r: int
    max_g: int
    max_b: int


def parse_line(line: str) -> GameRecord:
    id_str, record = line.split(':')
    id = int(id_str.replace('Game', '').strip())
    max_r, max_g, max_b = 0, 0, 0

    for round in record.split(';'):
        for count in round.split(','):
            i, color = count.strip().split(' ')
            if color == 'red':
                max_r = max(max_r, int(i))
            elif color == 'green':
                max_g = max(max_g, int(i))
            elif color == 'blue':
                max_b = max(max_b, int(i))

    game = GameRecord(id, max_r, max_g, max_b)
    logger.debug(f'{line}\n  {game}')
    return game


def is_valid_game(game: GameRecord) -> bool:
    return game.max_r <= 12 and game.max_g <= 13 and game.max_b <= 14


def solve(**kwargs) -> Solution:
    data = read_input(2, **kwargs)

    games = [parse_line(line) for line in data.splitlines()]
    valid_games = [g for g in games if is_valid_game(g)]
    answer_1 = sum([g.id for g in valid_games])
    logger.info(f'Part 1: {answer_1}')

    answer_2 = sum([g.max_r * g.max_g * g.max_b for g in games])
    logger.info(f'Part 2: {answer_2}')

    return answer_1, answer_2
