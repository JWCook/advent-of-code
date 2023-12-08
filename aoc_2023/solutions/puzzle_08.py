"""https://adventofcode.com/2023/day/8"""
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
        node_objs[name] = Node(name, None, None)

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
        # logger.debug(f'[{moves}] Moved {d} to {cur_node.name}')
        moves += 1
        if cur_node == end_node:
            logger.info(f'Found target node after {moves} moves')
            break
    return moves


def follow_ghost_directions(nodes: list[Node], directions: str) -> int:
    start_nodes = [node for node in nodes if node.name.endswith('A')]
    cur_nodes = start_nodes[:]
    end_state = 'Z' * len(start_nodes)

    moves = 0
    for d in cycle(directions):
        cur_nodes = [node.left if d == 'L' else node.right for node in cur_nodes]
        moves += 1
        state = "".join(node.name[-1] for node in cur_nodes)
        if moves % 1000000 == 0:
            logger.debug(f'[{moves}]: {state}')

        if state == end_state:
            logger.info(f'Found target nodes after {moves} moves')
            break
    return moves


def solve(**kwargs) -> Solution:
    data = read_input(2023, 8, **kwargs)
    nodes, directions = parse_list(data)
    moves_1 = follow_directions(nodes, directions)
    moves_2 = follow_ghost_directions(nodes, directions)
    return moves_1, moves_2
