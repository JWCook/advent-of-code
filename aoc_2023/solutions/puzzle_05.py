# Incomplete; brute force solution only
"""https://adventofcode.com/2023/day/5"""
import re
from concurrent.futures import ProcessPoolExecutor, as_completed
from os import getpid

from loguru import logger

from aoc_utils import Solution, chunkify, read_input

AgMap = list[tuple[int, ...]]


def parse_maps(data: str) -> tuple[list[int], list[AgMap]]:
    """Parse seeds and maps from input data.
    Seeds is a simple list, and each map is a list of tuples in the form:
    (dest_range_start, src_range_start, range_length)
    """

    def _split_ints(line):
        return [int(i) for i in line.split(' ')]

    def _parse_map(map):
        return [tuple(_split_ints(line)) for line in map.splitlines()]

    tokens = [t.strip() for t in re.split(r'([\sa-z-]+:)', data) if t.strip()]
    sections = dict(chunkify(tokens, 2))
    seeds = _split_ints(sections.pop('seeds:'))
    maps = [_parse_map(v) for v in sections.values()]
    return seeds, maps


def find_seed_location(seed: int, maps: list[AgMap]) -> int:
    """Follow maps from a given seed to a compatible location"""

    def check_map(find_src, map):
        for dest, src, length in map:
            if src <= find_src < src + length:
                return dest + find_src - src
        # If no explicit range matches, then the src value translates to dest 1:1
        return find_src

    search_val = seed
    for map in maps:
        search_val = check_map(search_val, map)
    return search_val


def min_location_for_seed_ranges(seeds: list[int], maps: list[AgMap]) -> int:
    """Find the minimum location for each seed range. At each map lookup step, we need to split
    each src range into multiple ranges that overlap with dest ranges.
    """
    avail_seed_ranges = sorted(chunkify(seeds, 2))
    logger.debug(f'Seed ranges: {avail_seed_ranges}')

    return 0


def min_location_for_seed_ranges_brute_force(seeds: list[int], maps: list[AgMap]) -> int:
    avail_seed_ranges = sorted(chunkify(seeds, 2))
    logger.debug(f'Seed ranges: {avail_seed_ranges}')

    min_location = None
    with ProcessPoolExecutor() as executor:
        futures = []
        for start, length in avail_seed_ranges:
            future = executor.submit(min_location_for_seed_range_brute_force, start, length, maps)
            futures.append(future)

        for future in as_completed(futures):
            location = future.result()
            if min_location is None or location < min_location:
                logger.info(f'New global min found: {min_location} -> {location}')
                min_location = location

    return min_location  # type: ignore


def min_location_for_seed_range_brute_force(start: int, length: int, maps: list[AgMap]) -> int:
    pid = getpid()
    logger.info(f'[{pid}] Starting worker ({start}-{start + length})')
    min_location = None

    for seed in range(start, start + length):
        logger.debug(f'[{pid}] {seed}')
        location = find_seed_location(seed, maps)
        if min_location is None or location < min_location:
            logger.info(f'[{pid}] New local min found: {min_location} -> {location}')
            min_location = location

    logger.info(f'[{pid}] Worker complete')
    return min_location  # type: ignore


def solve(**kwargs) -> Solution:
    data = read_input(2023, 5, **kwargs)
    seeds, maps = parse_maps(data)

    locations = [find_seed_location(seed, maps) for seed in seeds]
    answer_1 = min(locations)

    answer_2 = min_location_for_seed_ranges_brute_force(seeds, maps)
    return answer_1, answer_2
