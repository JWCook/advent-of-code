# Incomplete; brute force solution only
"""https://adventofcode.com/2023/day/5"""
import re

from loguru import logger

from aoc_utils import Solution, chunkify, read_input

INT_MAX = 2**32

Range = tuple[int, int]
AgMap = list[tuple[int, ...]]


def parse_maps(data: str) -> tuple[list[int], list[AgMap]]:
    """Parse seeds and maps from input data.

    Seeds is a simple list, and each map is a list of tuples in the form:
    (dest_range_start, src_range_start, range_length)

    Translate into:
    (range_start, range_end, src_to_dest_offset)
    """

    tokens = [t.strip() for t in re.split(r'([\sa-z-]+:)', data) if t.strip()]
    sections = dict(chunkify(tokens, 2))
    seeds = _split_ints(sections.pop('seeds:'))
    maps = [parse_map(v) for v in sections.values()]
    logger.debug('\n\n'.join([str(m) for m in maps]))
    return seeds, maps


def parse_map(map_str: str) -> AgMap:
    """
    Translate a map in the form:
    (dest_range_start, src_range_start, range_length)

    Into:
    (range_start, range_end, src_to_dest_offset)

    And add additional ranges to fill in gaps between ranges.
    """
    # Parse, translate, and sort
    orig_map = [_split_ints(line) for line in map_str.splitlines()]
    map = [(src, src + length, dest - src) for dest, src, length in orig_map]
    map = sorted(map)

    # Add start and end gaps (not strictly necessary, but makes things simpler)
    gap_ranges: list[Range] = []
    if map[0][0] > 0:
        gap_ranges.append((0, map[0][0] - 1))
    gap_ranges.append((map[-1][1], INT_MAX))

    # Add gaps in between ranges
    last_end = map[0][1]
    for start, end, _ in map[1:]:
        if start > last_end + 1:
            gap_ranges.append((last_end + 1, start - 1))
        last_end = end

    # Add these gaps with offset 0 and sort
    return sorted(map + [(start, end, 0) for start, end in gap_ranges])


def _split_ints(line: str) -> list[int]:
    return [int(i) for i in line.split(' ')]


def min_location_for_seeds(seeds: list[int], maps: list[AgMap]) -> int:
    """Part 1: Find the minimum location for set of starting seeds"""
    return min([find_seed_location(seed, maps) for seed in seeds])


def find_seed_location(seed: int, maps: list[AgMap]) -> int:
    """Follow maps from a given seed to a compatible location"""
    search_val = seed
    for map in maps:
        for start, end, offset in map:
            if start <= search_val < end:
                search_val = search_val + offset
                break
    return search_val


def min_location_for_seed_ranges(seeds: list[int], maps: list[AgMap]) -> int:
    """Part 2: Find the minimum location for a set of seed ranges"""
    seed_ranges = [(start, start + length) for start, length in sorted(chunkify(seeds, 2))]
    logger.debug(f'Seed ranges: {seed_ranges}')

    locations = []
    for start, end in seed_ranges:
        src_ranges = [(start, end)]
        for map in maps:
            src_ranges = get_range_overlaps(src_ranges, map)
        locations.append(min([start for start, _ in src_ranges]))
    return min(locations)


def get_range_overlaps(src_ranges: list[Range], dest_map: AgMap) -> list[Range]:
    """Given multiple source ranges and destination ranges, get all ranges of overlapping values"""
    overlaps = []
    for start_1, end_1 in src_ranges:
        for start_2, end_2, offset in dest_map:
            if not (start_1 > end_2 or end_1 < start_2):
                overlaps.append((max(start_1, start_2) + offset, min(end_1, end_2) + offset))
    logger.debug(f'Overlaps between {src_ranges} and {dest_map}: {overlaps}')
    return overlaps


def solve(**kwargs) -> Solution:
    data = read_input(2023, 5, **kwargs)
    seeds, maps = parse_maps(data)
    answer_1 = min_location_for_seeds(seeds, maps)
    answer_2 = min_location_for_seed_ranges(seeds, maps)
    return answer_1, answer_2
