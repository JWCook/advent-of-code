"""https://adventofcode.com/2023/day/13"""
import re
from collections import deque

from loguru import logger

from aoc_utils import Solution, read_input


def find_mirror_vertical(stage: list[str]) -> int:
    rotated = [''.join(c) for c in zip(*stage, strict=True)]
    idx = find_mirror_horizontal(rotated)
    return idx


def find_mirror_horizontal(stage: list[str]) -> int:
    prev_line = stage[0]
    for i, line in enumerate(stage[1:]):
        if line == prev_line and validate_mirror_line(stage, i):
            logger.debug(f'Found line: {i} ({line})')
            return i + 1
        prev_line = line
    return 0

def validate_mirror_line(stage: list[str], idx: int) -> bool:
    logger.debug(f'Validate mirror line {idx} ({stage[idx]})')
    for i in range(1, len(stage)-idx):
        logger.debug(f'Compare {idx+i} & {idx-i+1}:\n{stage[idx+i]}\n{stage[idx-i+1]}')
        try:
            if idx-i+1 < 0:
                raise IndexError
            if stage[idx+i] != stage[idx-i+1]:
                logger.debug('  Not a match')
                return False
        except IndexError:
            return True
    return True


def mirror_score(stage: list[str]) -> int:
    if n_cols := find_mirror_horizontal(stage):
        score =  n_cols * 100
    else:
        score =  find_mirror_vertical(stage)
    logger.debug(f'Score: {score}')
    return score


def solve(**kwargs) -> Solution:
    data = read_input(2023, 13, **kwargs)
    stages = [s.strip().splitlines() for s in  re.split(r'\n\n', data)]
    total_score = sum(mirror_score(s) for s in stages)
    return (total_score, None)