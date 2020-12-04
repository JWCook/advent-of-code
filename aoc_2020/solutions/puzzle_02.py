#!/usr/bin/env python3
import re
from logging import getLogger
from typing import List, Tuple

from solutions import get_input_data

LINE_PATTERN = re.compile(r'([0-9]+)-([0-9]+)+\s*(\w):\s*(\S+)')
InputLine = Tuple[int, int, str, str]
logger = getLogger(__file__)


def main():
    input_data = get_input_data(2)
    input_lines = [parse_line(line) for line in input_data]

    valid_passwords_a = [line[3] for line in input_lines if line and is_valid_r1(*line)]
    logger.info(
        f'Solution 2a: {len(valid_passwords_a)} out of {len(input_data)} passwords are valid'
    )

    valid_passwords_b = [line[3] for line in input_lines if line and is_valid_r2(*line)]
    logger.info(
        f'Solution 2b: {len(valid_passwords_b)} out of {len(input_data)} passwords are valid'
    )


def parse_line(line: str) -> InputLine:
    """Parse an input line into min, max, character, password"""
    line = line.strip()
    if not line:
        return None

    match = LINE_PATTERN.match(line)
    if not match:
        logger.warning(f'Invalid line: {line}')
        return None

    char_min, char_max, required_char, password = match.groups()
    return int(char_min), int(char_max), required_char, password


def is_valid_r1(char_min: int, char_max: int, required_char: str, password: str) -> bool:
    """Test if a password meets the given requirements, according to rule #1"""
    char_count = password.count(required_char)
    is_valid = char_min <= char_count <= char_max
    if not is_valid:
        logger.debug(
            f"Invalid: '{password}' contains '{required_char}' {char_count} times; "
            f'requires {char_min}-{char_max}'
        )
    return is_valid


def is_valid_r2(pos_1: int, pos_2: int, required_char: str, password: str) -> bool:
    """Test if a password meets the given requirements, according to rule #2"""
    # Provided index starts at 1
    pos_1 -= 1
    pos_2 -= 1

    try:
        has_char_1 = password[pos_1] == required_char
        has_char_2 = password[pos_2] == required_char
        is_valid = has_char_1 != has_char_2  # XOR
    except IndexError as e:
        logger.error(str(e))
        return False

    if not is_valid:
        logger.debug(
            f"Invalid: '{password}' contains {password[pos_1]} and {password[pos_2]} "
            f"at indices {pos_1}, {pos_2}; requires '{required_char}' exactly once"
        )
    return is_valid


if __name__ == '__main__':
    main()
