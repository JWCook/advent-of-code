"""https://adventofcode.com/2023/day/12"""
import re
from dataclasses import dataclass
from itertools import combinations, product

from loguru import logger

from aoc_utils import Solution, read_input


@dataclass
class Record:
    row: str
    groups: list[int]


def parse_records(data:str) -> list[Record]:
    records = []
    for line in data.splitlines():
        row, groups = line.split(' ')
        groups = [int(group) for group in groups.split(',')]
        records.append(Record(row, groups))
    return records


def expand_records(records: list[Record]) -> list[Record]:
    for record in records:
        record.row *= 5
        record.groups *=5
    return records


def get_group_sizes(row:str) -> list[int]:
    return [len(g) for g in re.split('\.+', row) if g]

def n_combinations(record: Record) -> int:
    """Return the number of possible combinations for a given row"""
    unknown_idxs = [i for i, c in enumerate(record.row) if c == '?']
    logger.debug(record)
    n_hashes = sum(record.groups) - record.row.count('#')
    possible_groups = [''.join(g) for g in product('.#', repeat=len(unknown_idxs)) if g.count('#') == n_hashes]
    n_valid_combinations = 0

    for group in possible_groups:
        candidate_row = list(record.row)
        for j, idx in enumerate(unknown_idxs):
            candidate_row[idx] = group[j]
        logger.debug(f"{''.join(candidate_row)} {get_group_sizes(''.join(candidate_row))}")
        if get_group_sizes(''.join(candidate_row)) == record.groups:
            n_valid_combinations += 1

    return n_valid_combinations





def solve(**kwargs) -> Solution:
    data = read_input(2023, 12, **kwargs)
    records = parse_records(data)
    logger.debug(records)
    # logger.info(n_combinations(records[0]))
    n_combos_1 = 0
    # for record in records:
    #     n = n_combinations(record)
    #     logger.info(n)
    #     n_combos_1 += n
    # logger.info(n_combos_1)

    records = expand_records(records)
    # for record in records:
    #     logger.info(record)
    n_combos_2 = 0
    for i, record in enumerate(records):
        n = n_combinations(record)
        logger.info(f'{i}: {n}')
        n_combos_2 += n
    logger.info(n_combos_2)

    return (n_combos_1, n_combos_2)