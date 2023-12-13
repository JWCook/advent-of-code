"""https://adventofcode.com/2023/day/12"""
import re
from dataclasses import dataclass
from functools import cache
from itertools import product

from loguru import logger

from aoc_utils import Solution, read_input


@dataclass
class Record:
    row: str
    groups: list[int]


def parse_records(data: str) -> list[Record]:
    records = []
    for line in data.splitlines():
        row, group_str = line.split(' ')
        groups = [int(group) for group in group_str.split(',')]
        records.append(Record(row, groups))
    logger.debug(records)
    return records


def expand_records(records: list[Record]) -> list[Record]:
    for record in records:
        record.row += f'?{record.row}' * 4
        record.groups *= 5
    return records


def find_combos(record: Record) -> int:
    """Return the number of possible combinations for a given row (naive method)"""
    unknown_idxs = [i for i, c in enumerate(record.row) if c == '?']
    logger.debug(record)
    n_hashes = sum(record.groups) - record.row.count('#')
    n_combos = 0

    pattern = re.compile('\.*' + '\.+'.join(['#' * i for i in record.groups]) + '\.*$')
    logger.debug(pattern)

    for group in (
        ''.join(g) for g in product('.#', repeat=len(unknown_idxs)) if g.count('#') == n_hashes
    ):
        candidate_row = list(record.row)
        for j, idx in enumerate(unknown_idxs):
            candidate_row[idx] = group[j]
        if pattern.match(''.join(candidate_row)):
            n_combos += 1

    return n_combos


@cache
def find_combos_2(segment: str, group_sizes: tuple[int]) -> int:  # type: ignore
    """Return the number of possible combinations for a given row (memoized recursive method)"""
    # Base case: reached the end of the row
    if len(segment) == 0:
        return 1 if len(group_sizes) == 0 else 0

    target_size = group_sizes[0] if group_sizes else 0

    match segment[0]:
        case '#':
            # Dead ends
            # fmt: off
            if (
                target_size == 0                                                # no more groups to match
                or '.' in segment[0:target_size]                                # group is interrupted
                or len(segment) < target_size                                   # segment is too short
                or (len(segment) > target_size and segment[target_size] == '#') # consecutive '#'s too long
            ):
                return 0
            # Found a match; move on to the next group
            else:
                return find_combos_2(segment[target_size + 1 :], group_sizes[1:])
        # Skip char
        case '.':
            return find_combos_2(segment[1:], group_sizes)
        # Find matches with both possible values for '?'
        case '?':
            n_combos = find_combos_2(f'#{segment[1:]}', group_sizes)
            return n_combos + find_combos_2(f'.{segment[1:]}', group_sizes)


def solve(**kwargs) -> Solution:
    data = read_input(2023, 12, **kwargs)
    records = parse_records(data)

    n_combos_1 = sum(find_combos(record) for record in records)
    n_combos_2 = sum(
        find_combos_2(record.row, tuple(record.groups)) for record in expand_records(records)
    )
    return (n_combos_1, n_combos_2)
