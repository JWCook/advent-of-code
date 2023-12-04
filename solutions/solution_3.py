#!/usr/bin/env python3
# https://adventofcode.com/2023/day/3
import re

from loguru import logger

from . import read_input

PART_CHAR = re.compile(r'.*[^\d\.]+.*')


def get_number_indexes(line: str) -> list[tuple[int, int]]:
    """Get start and end index of each number (consecutive digits) in the line"""
    # Get each digit character and its index
    digit_idxs = [i for i, c in enumerate(line) if c.isdigit()]
    if not digit_idxs:
        return []

    # Get start and end index of each number (group of consecutive digits)
    number_idxs = []
    start_idx = digit_idxs[0]
    prev_idx = 0
    for idx in digit_idxs:
        # Start new number and add previous one
        if idx - prev_idx > 1:
            if prev_idx - start_idx >= 0:
                number_idxs.append((start_idx, prev_idx + 1))
            start_idx = idx
        prev_idx = idx

    if prev_idx - start_idx > 0:
        number_idxs.append((start_idx, prev_idx + 1))
    return number_idxs


def is_part_number(
    line: str,
    prev_line: str,
    next_line: str,
    start_idx: int,
    end_idx: int,
) -> bool:
    # Get a rectangle of characters adjacent to the part number (including diagonals)
    adj_start_idx = max(0, start_idx - 1)
    adj_end_idx = min(len(line), end_idx + 1)
    in_range = [prev_line[adj_start_idx:adj_end_idx]]
    in_range.append(line[adj_start_idx:adj_end_idx])
    in_range.append(next_line[adj_start_idx:adj_end_idx])

    is_valid = bool(PART_CHAR.match(''.join(in_range)))
    logger.debug('\n' + '\n'.join(in_range))
    logger.debug(f'{line[start_idx:end_idx]} is valid: {is_valid}')
    return is_valid


def get_valid_part_numbers(data: str):
    lines = data.splitlines()
    number_idxs = [get_number_indexes(line) for line in lines]

    part_numbers = []
    for i, start_idx, end_idx in [
        (i, start_idx, end_idx)
        for i, line_idxs in enumerate(number_idxs)
        for start_idx, end_idx in line_idxs
    ]:
        prev_line = lines[i - 1] if i > 0 else ''
        next_line = lines[i + 1] if i < len(lines) - 1 else ''
        if is_part_number(lines[i], prev_line, next_line, start_idx, end_idx):
            part_numbers.append(int(lines[i][start_idx:end_idx]))

    logger.debug(part_numbers)
    return part_numbers


if __name__ == '__main__':
    data = read_input('3')
    part_numbers = get_valid_part_numbers(data)
    logger.info(f'Part 1: {sum(part_numbers)}')
