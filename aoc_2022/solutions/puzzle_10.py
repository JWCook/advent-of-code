# https://adventofcode.com/2022/day/10
from . import Solution, read_input


def parse_cycles(data: str) -> list[int]:
    cycles = [1]
    x = 1

    for line in data.splitlines():
        cycles.append(x)
        if line.startswith('addx'):
            x += int(line.split()[1])
            cycles.append(x)

    return cycles


def get_total_signal_strength(cycles: list[int]) -> int:
    signal_strengths = [(i + 1) * x for i, x in enumerate(cycles)]
    idxs = [20, 60, 100, 140, 180, 220]
    return sum([signal_strengths[idx - 1] for idx in idxs])


def get_pixels(cycles: list[int]) -> str:
    pixels = ''
    for i, x in enumerate(cycles):
        pixel = i % 40
        if (pixel - 1) <= x <= pixel + 1:
            pixels += '#'
        else:
            pixels += '.'
    return pixels


def format_pixels(pixels: str) -> str:
    grid = []
    idx = 0
    while idx < len(pixels):
        grid.append(pixels[idx : idx + 40])
        idx += 40
    return '\n'.join(grid)


def solve(**kwargs) -> Solution:
    data = read_input(10, **kwargs)
    cycles = parse_cycles(data)
    answer_1 = get_total_signal_strength(cycles)

    pixels = get_pixels(cycles)
    answer_2 = format_pixels(pixels)
    return answer_1, '\n' + answer_2
