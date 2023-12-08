"""https://adventofcode.com/2023/day/8"""
import math
from dataclasses import dataclass
from itertools import cycle

from loguru import logger

from aoc_utils import Solution, read_input


@dataclass
class Node:
    name: str
    left: 'Node'
    right: 'Node'


def parse_list(data: str) -> tuple[list[Node], str]:
    node_strs = {}
    node_objs = {}
    lines = data.splitlines()
    directions = lines[0]

    for line in lines[2:]:
        name, children = line.split(' = ')
        node_strs[name] = children.strip('()').split(', ')
        node_objs[name] = Node(name, None, None)  # type: ignore

    for name, (left_name, right_name) in reversed(node_strs.items()):
        node_objs[name].left = node_objs[left_name]
        node_objs[name].right = node_objs[right_name]
    return list(reversed(node_objs.values())), directions


def follow_directions(nodes: list[Node], directions: str) -> int:
    nodes_dict = {node.name: node for node in nodes}
    start_node = nodes_dict['AAA']
    end_node = nodes_dict['ZZZ']
    cur_node = start_node

    moves = 0
    for d in cycle(directions):
        cur_node = cur_node.left if d == 'L' else cur_node.right
        moves += 1
        if cur_node == end_node:
            logger.info(f'Found target node after {moves} moves')
            break
    return moves


def follow_ghost_directions(nodes: list[Node], directions: str) -> int:
    start_nodes = [node for node in nodes if node.name.endswith('A')]
    cycle_lengths = []

    for i, node in enumerate(start_nodes):
        cur_node = node
        moves = 0
        for d in cycle(directions):
            cur_node = cur_node.left if d == 'L' else cur_node.right
            moves += 1
            if cur_node.name.endswith('Z'):
                logger.info(f'[{i} Found target nodes after {moves} moves')
                cycle_lengths.append(moves)
                break

    return math.lcm(*cycle_lengths)


def solve(**kwargs) -> Solution:
    data = read_input(2023, 8, **kwargs)
    nodes, directions = parse_list(data)
    return (
        follow_directions(nodes, directions),
        follow_ghost_directions(nodes, directions),
    )
