"""https://adventofcode.com/2023/day/13"""
import re

from loguru import logger

from aoc_utils import Solution, read_input


def find_mirror_vertical(stage: list[str], skip: int = -1) -> int:
    rotated = [''.join(c) for c in zip(*stage, strict=True)]
    return find_mirror_horizontal(rotated, skip=skip)


def find_mirror_horizontal(stage: list[str], skip: int = -1) -> int:
    prev_line = stage[0]
    for i, line in enumerate(stage[1:]):
        if line == prev_line and (i + 1 != skip) and validate_mirror_line(stage, i):
            logger.debug(f'Found mirro line: {i} ({line})')
            return i + 1
        prev_line = line
    return 0


def validate_mirror_line(stage: list[str], idx: int) -> bool:
    logger.debug(f'Validate mirror line {idx} ({stage[idx]})')

    for i in range(1, len(stage) - idx):
        logger.debug(f'Compare {idx+i} & {idx-i+1}:\n{stage[idx+i]}\n{stage[idx-i+1]}')
        try:
            opposite_idx = idx - i + 1
            if opposite_idx < 0:
                raise IndexError
            if stage[idx + i] != stage[opposite_idx]:
                logger.debug('  Not a match')
                return False
        # Reached the edge; no more comparisons needed
        except IndexError:
            return True

    return True


def find_mirror(stage, skip=(None, -1)) -> tuple[str, int, int]:
    # skip = axis and index of previously found mirror line
    skip_h = skip[1] if skip[0] == 'h' else -1
    skip_v = skip[1] if skip[0] == 'v' else -1
    if idx := find_mirror_horizontal(stage, skip_h):
        return ('h', idx, idx * 100)
    else:
        idx = find_mirror_vertical(stage, skip_v)
        return ('v', idx, idx)


def find_alt_mirror(stage: list[str]) -> int:
    mirror_idx = find_mirror(stage)[:2]

    # Try flipping each bit and test if a different mirror line is found
    for i in range(len(stage[0])):
        for j in range(len(stage)):
            flipped_bit = '.' if stage[j][i] == '#' else '#'
            flipped_line = stage[j][:i] + flipped_bit + stage[j][i + 1 :]
            axis, idx, score = find_mirror(
                stage[:j] + [flipped_line] + stage[j + 1 :], skip=mirror_idx
            )

            if idx and (axis, idx) != mirror_idx:
                logger.info(f'New idx: {idx} ({axis}: {i}, {j})')
                return score

    raise ValueError


def solve(**kwargs) -> Solution:
    data = read_input(2023, 13, **kwargs)
    stages = [s.strip().splitlines() for s in re.split(r'\n\n', data)]
    return (
        sum(find_mirror(s)[-1] for s in stages),
        sum(find_alt_mirror(s) for s in stages),
    )
