# https://adventofcode.com/2022/day/3
from . import Solution, read_input


def char_priority(char: str) -> int:
    """Get character priority using offset from Unicode code point
    Priority: a-z: 1-26, A-Z: 27-52
    """
    offset = 96 if char.islower() else 38
    return ord(char) - offset


def get_str_common_item(line: str) -> str:
    """Get the character that appears in both halves of a string"""
    i = len(line) // 2
    pack_1 = set(line[:i])
    pack_2 = set(line[i:])
    return list(pack_1 & pack_2)[0]


def get_lines_common_item(*lines: str) -> str:
    """Get the character that appears in all specified lines"""
    intersection = set(lines[0])
    for line in lines[1:]:
        intersection &= set(line.strip())
    return list(intersection)[0]


def get_pack_total_priority(data: str) -> int:
    total_priority = 0
    for line in data.splitlines():
        common_item = get_str_common_item(line)
        total_priority += char_priority(common_item)
    return total_priority


def get_badge_total_priority(data: str) -> int:
    total_priority = 0
    lines = iter(data.splitlines())
    while True:
        try:
            common_item = get_lines_common_item(next(lines), next(lines), next(lines))
            total_priority += char_priority(common_item)
        except StopIteration:
            break
    return total_priority


def solve(**kwargs) -> Solution:
    data = read_input(3, **kwargs)
    return (
        get_pack_total_priority(data),
        get_badge_total_priority(data),
    )
