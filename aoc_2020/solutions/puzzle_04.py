#!/usr/bin/env python3
import re
from logging import getLogger

from solutions import get_input_data

logger = getLogger(__file__)


REQUIRED_FIELDS = {
    'byr': 'Birth Year',  # four digits; at least 1920 and at most 2002.
    'iyr': 'Issue Year',  # four digits; at least 2010 and at most 2020.
    'eyr': 'Expiration Year',  # four digits; at least 2020 and at most 2030.
    'hgt': 'Height',  # a number followed by either cm (150-193) or in (59-76)
    'hcl': 'Hair Color',  # # followed by exactly six characters 0-9 or a-f.
    'ecl': 'Eye Color',  # exactly one of: amb blu brn gry grn hzl oth.
    'pid': 'Passport ID',  # a nine-digit number, including leading zeroes.
}
OPTIONAL_FIELDS = {'cid': 'Country ID'}

EYE_COLORS = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
HAIR_COLOR_PATTERN = re.compile(r'\#([0-9a-f]{6})')
HEIGHT_RANGES = {'cm': (150, 193), 'in': (59, 76)}


def main():
    input_data = get_input_data(4, split=False)
    passports = parse_passports(input_data)
    valid_passports = get_valid_passports_r1(passports)
    logger.info(f'Solution 4a: {len(valid_passports)} out of {len(passports)} passports are valid')

    valid_passports = get_valid_passports_r2(valid_passports)
    logger.info(f'Solution 4b: {len(valid_passports)} out of {len(passports)} passports are valid')


def parse_passports(input_data):
    chunks = input_data.split('\n\n')
    logger.info(f'Found {len(chunks)} chunks of text in {len(input_data.splitlines())} total lines')
    return [parse_passport(chunk) for chunk in chunks]


def parse_passport(chunk):
    """Parse a single chunk of text into passport fields"""
    # Split fields by either single newline or space; then split fields into key-value pairs
    fields = [field.split(':') for field in chunk.split()]
    return {field[0]: field[1] for field in fields}


def get_valid_passports_r1(passports):
    """Get all valid passports, according to the rule in part 1"""

    def validate_passport(passport):
        return all([field in passport for field in REQUIRED_FIELDS])

    return [p for p in passports if validate_passport(p)]


def get_valid_passports_r2(passports):
    """Get all valid passports, according to the rules in part 2"""
    return [p for p in passports if validate_passport_r2(p)]


def validate_passport_r2(passport):
    try:
        assert 1920 <= int(passport['byr']) <= 2002
        assert 2010 <= int(passport['iyr']) <= 2020
        assert 2020 <= int(passport['eyr']) <= 2030
        assert HAIR_COLOR_PATTERN.match(passport['hcl'])
        assert validate_height(passport['hgt'])
        assert passport['ecl'] in EYE_COLORS
        assert len(passport['pid']) == 9 and int(passport['pid'])
    except (AssertionError, TypeError) as e:
        logger.debug(str(e))
        return False

    return True


def validate_height(height_str):
    value, unit = height_str[:-2], height_str[-2:]
    assert unit in HEIGHT_RANGES

    h_min, h_max = HEIGHT_RANGES[unit]
    assert h_min <= int(value) <= h_max
    return True


if __name__ == '__main__':
    main()
