"""https://adventofcode.com/2023/day/13"""
import re

from loguru import logger

from aoc_utils import Solution, read_input


def find_mirror_vertical(stage: list[str], skip: int = -1) -> int:
    rotated = [''.join(c) for c in zip(*stage, strict=True)]
    idx = find_mirror_horizontal(rotated, skip=skip)
    return idx


def find_mirror_horizontal(stage: list[str], skip: int = -1) -> int:
    prev_line = stage[0]
    for i, line in enumerate(stage[1:]):
        if line == prev_line and (i + 1 != skip) and validate_mirror_line(stage, i):
            logger.debug(f'Found line: {i} ({line})')
            return i + 1
        prev_line = line
    return 0


def validate_mirror_line(stage: list[str], idx: int) -> bool:
    logger.debug(f'Validate mirror line {idx} ({stage[idx]})')
    for i in range(1, len(stage) - idx):
        logger.debug(f'Compare {idx+i} & {idx-i+1}:\n{stage[idx+i]}\n{stage[idx-i+1]}')
        try:
            if idx - i + 1 < 0:
                raise IndexError
            if stage[idx + i] != stage[idx - i + 1]:
                logger.debug('  Not a match')
                return False
        except IndexError:
            return True
    return True


def mirror_score(stage: list[str]) -> int:
    if n_cols := find_mirror_horizontal(stage):
        score = n_cols * 100
    else:
        score = find_mirror_vertical(stage)
    logger.debug(f'Score: {score}')
    return score


def get_mirror_idx(stage, skip=(None, -1)):
    axis, idx = skip
    if n_cols := find_mirror_horizontal(stage, skip=idx if axis == 'h' else None):
        return ('h', n_cols)
    else:
        n_cols = find_mirror_vertical(stage, skip=idx if axis == 'v' else None)
        return ('v', n_cols)


def mirror_score_2(stage: list[str]) -> int:
    mirror_idx = get_mirror_idx(stage)

    for i in range(len(stage[0])):
        for j in range(len(stage)):
            logger.debug(f'Testing {i}, {j}')
            stage2 = [list(s) for s in stage]
            stage2[j][i] = '.' if stage2[j][i] == '#' else '#'
            test_mirror_idx = get_mirror_idx([''.join(s) for s in stage2], skip=mirror_idx)
            if test_mirror_idx[1] and test_mirror_idx != mirror_idx:
                axis, score = test_mirror_idx
                new_score = score * 100 if axis == 'h' else score
                logger.info(f'New score: {new_score} ({axis}: {i}, {j})')
                return new_score

    raise ValueError


def solve(**kwargs) -> Solution:
    data = read_input(2023, 13, **kwargs)
    stages = [s.strip().splitlines() for s in re.split(r'\n\n', data)]
    return (
        sum(mirror_score(s) for s in stages),
        sum(mirror_score_2(s) for s in stages),
    )
