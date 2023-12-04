#!/usr/bin/env python
# https://adventofcode.com/2023/day/3
import re
from dataclasses import dataclass

from loguru import logger

from solutions.utils import read_input

PART_CHAR = re.compile(r'.*[^\d\.]+.*')


@dataclass
class Part:
    id: int
    x1: int
    x2: int
    y: int

    def adjacency_box(self) -> tuple[int, int, int, int]:
        return (self.x1 - 1, self.y - 1, self.x2 + 1, self.y + 1)

    def is_adjacent(self, x: int, y: int) -> bool:
        x_min, y_min, x_max, y_max = self.adjacency_box()
        return x_min <= x <= x_max and y_min <= y <= y_max


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
                number_idxs.append((start_idx, prev_idx))
            start_idx = idx
        prev_idx = idx

    if prev_idx - start_idx > 0:
        number_idxs.append((start_idx, prev_idx))
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
    adj_end_idx = min(len(line), end_idx + 2)
    in_range = [prev_line[adj_start_idx:adj_end_idx]]
    in_range.append(line[adj_start_idx:adj_end_idx])
    in_range.append(next_line[adj_start_idx:adj_end_idx])

    is_valid = bool(PART_CHAR.match(''.join(in_range)))
    logger.debug('\n' + '\n'.join(in_range))
    logger.debug(f'{line[start_idx:end_idx+1]} is valid: {is_valid}')
    return is_valid


def get_valid_parts(data: str) -> list[Part]:
    lines = data.splitlines()
    number_idxs = [get_number_indexes(line) for line in lines]

    parts = []
    for y, line_idxs in enumerate(number_idxs):
        for x1, x2 in line_idxs:
            prev_line = lines[y - 1] if y > 0 else ''
            next_line = lines[y + 1] if y < len(lines) - 1 else ''
            if is_part_number(lines[y], prev_line, next_line, x1, x2):
                parts.append(Part(int(lines[y][x1 : x2 + 1]), x1, x2, y))

    logger.debug([part.id for part in parts])
    return parts


def get_asterisk_coords(data: str) -> list[tuple[int, int]]:
    lines = data.splitlines()
    asterisk_coords = []
    for y, line in enumerate(lines):
        x = -1
        while True:
            try:
                x = line.index('*', x + 1)
                asterisk_coords.append((x, y))
            except ValueError:
                break

    logger.debug(asterisk_coords)
    return asterisk_coords


def get_gear_values(parts: list[Part], asterisk_coords: list[tuple[int, int]]) -> list[int]:
    gear_values = []
    for x, y in asterisk_coords:
        adjacent_part_ids = [part.id for part in parts if part.is_adjacent(x, y)]
        if len(adjacent_part_ids) == 2:
            logger.debug(
                f'{x}, {y} is a gear with value {adjacent_part_ids[0]} * {adjacent_part_ids[1]} = '
                f'{adjacent_part_ids[0] * adjacent_part_ids[1]}'
            )
            gear_values.append(adjacent_part_ids[0] * adjacent_part_ids[1])
    return gear_values


def solve(**kwargs):
    data = read_input(3, **kwargs)
    parts = get_valid_parts(data)
    answer_1 = sum([part.id for part in parts])
    logger.info(f'Part 1: {answer_1}')

    asterisk_coords = get_asterisk_coords(data)
    gears = get_gear_values(parts, asterisk_coords)
    answer_2 = sum(gears)
    logger.info(f'Part 2: {answer_2}')
