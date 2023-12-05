# Incomplete; brute force solution only
"""https://adventofcode.com/2023/day/5"""
from concurrent.futures import ProcessPoolExecutor, as_completed
from hashlib import blake2b
from os import getpid

from loguru import logger

from . import Solution, read_input
from .input_05 import all_maps, seeds


def find_seed_location(seed: int) -> int:
    search_val = seed
    for map in all_maps:
        search_val = check_map(search_val, map)
    return search_val


def check_map(find_src: int, map: list[list]):
    """Find dest given src"""
    for dest, src, length in map:
        if src <= find_src < src + length:
            diff = find_src - src
            return dest + diff
    return find_src


def get_seed_ranges() -> list[tuple[int, int]]:
    """split seeds into (start, end) pairs"""
    ranges = []
    for i in range(0, len(seeds), 2):
        ranges.append((seeds[i], seeds[i] + seeds[i + 1]))
    return sorted(ranges, key=lambda x: x[0])


def min_location_for_seed_ranges_brute_force() -> int:
    avail_seed_pairs = get_seed_ranges()

    min_location = None
    with ProcessPoolExecutor() as executor:
        futures = []
        for start, end in avail_seed_pairs:
            future = executor.submit(min_location_for_seed_range_brute_force, start, end)
            futures.append(future)

        for future in as_completed(futures):
            location = future.result()
            if min_location is None or location < min_location:
                logger.info(f'New global min found: {min_location} -> {location}')
                min_location = location

    assert min_location is not None
    return min_location


def _short_hash(value) -> str:
    return blake2b(str(value).encode(), digest_size=4).hexdigest()


def min_location_for_seed_range_brute_force(start, end) -> int:
    # thread_id = _short_hash(threading.get_ident())
    pid = getpid()
    logger.info(f'[{pid}] Starting worker ({start}-{end})')
    min_location = None

    for seed in range(start, end):
        location = find_seed_location(seed)
        if min_location is None or location < min_location:
            logger.info(f'[{pid}] New local min found: {min_location} -> {location}')
            min_location = location

    logger.info(f'[{pid}] Worker complete')
    assert min_location is not None
    return min_location


def solve(**kwargs) -> Solution:
    data = read_input(5, **kwargs)
    logger.debug(data)
    locations = [find_seed_location(seed) for seed in seeds]
    answer_1 = min(locations)

    if kwargs.get('test'):
        return answer_1, None

    # answer_2 = min_location_for_seed_ranges()
    answer_2 = min_location_for_seed_ranges_brute_force()
    return answer_1, answer_2
