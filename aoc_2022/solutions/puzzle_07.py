#!/usr/bin/env python3
# https://adventofcode.com/2022/day/7
from dataclasses import dataclass, field

from loguru import logger

from . import read_input

FS_SIZE = 70000000
SPACE_REQUIRED = 30000000


@dataclass
class Node:
    name: str = field()


@dataclass
class Directory(Node):
    parent: 'Directory' = field(default=None)
    children: list['Node'] = field(default_factory=list)
    total_size: int = field(default=None)

    def add_node(self, node: 'Node'):
        self.children.append(node)

    def get_node(self, name: str) -> 'Node':
        for child in self.children:
            if child.name == name:
                return child
        raise ValueError(name)

    def get_size(self) -> int:
        if not self.total_size:
            self.total_size = sum(child.get_size() for child in self.children)
        return self.total_size

    def get_subdirs(self) -> list['Directory']:
        return [child for child in self.children if isinstance(child, Directory)]


@dataclass
class File(Node):
    size: int = field(default=0)

    def get_size(self) -> int:
        return self.size


def count_directory_sizes(cmd_output: str) -> Directory:
    root = Directory(name='/')
    pwd = root
    for line in cmd_output.splitlines():
        line = line.strip()
        if line == '$ cd /' or line == '$ ls':
            pass
        elif line.startswith('$ cd '):
            name = line[5:]
            if name == '..':
                pwd = pwd.parent
            else:
                pwd = pwd.get_node(name)
        elif line.startswith('dir '):
            pwd.add_node(Directory(name=line[4:], parent=pwd))
        elif line[0].isdigit():
            size, name = line.split()
            pwd.add_node(File(name=name, size=int(size)))
        else:
            raise ValueError(line)
    return root


def get_subdir_totals(root: Directory, lvl: int = 0) -> int:
    total = 0
    sz = root.get_size()
    if sz <= 100000:
        total += sz
    padding = '  ' * lvl
    logger.debug(f'{padding} {root.name}: {sz}')

    for subdir in root.get_subdirs():
        total += get_subdir_totals(subdir, lvl=lvl + 1)
    return total


def find_dir_to_delete(root: Directory) -> Directory:
    space_to_delete = SPACE_REQUIRED - (FS_SIZE - root.get_size())
    dirs = sorted(find_candidate_dirs(root, space_to_delete), key=lambda d: d.get_size())
    return dirs[0]


def find_candidate_dirs(root: Directory, space_to_delete: int) -> list[Directory]:
    candidate_dirs = []
    if root.get_size() > space_to_delete:
        candidate_dirs.append(root)
    for subdir in root.get_subdirs():
        candidate_dirs.extend(find_candidate_dirs(subdir, space_to_delete))
    return candidate_dirs


if __name__ == '__main__':
    data = read_input(7)
    root = count_directory_sizes(data)
    logger.info(f'Part 1: {get_subdir_totals(root)}')
    logger.info(f'Part 2: {find_dir_to_delete(root).get_size()}')
