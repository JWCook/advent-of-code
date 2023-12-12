# https://adventofcode.com/2022/day/11
import re
from dataclasses import dataclass, field
from typing import Callable, Iterator

from loguru import logger

from . import Solution, read_input

MonkeyMap = dict[int, 'Monkey']
MONKEY_PATTERN = re.compile(
    r'(\d+):\n\s+Starting items: (.+)\n\s*'
    r'Operation: new = (.*)\n\s*'
    r'Test: divisible by (.+)\n\s*'
    r'If true: throw to monkey (\d+)\n\s*'
    r'If false: throw to monkey (\d+)',
    re.MULTILINE,
)


@dataclass
class Monkey:
    id: int = field()
    items: list[int] = field()
    operation: Callable = field()
    test_divisible: int = field()
    next_true: int = field()
    next_false: int = field()
    n_inspected: int = field(default=0)
    modulo: int = field(default=0)
    divide_after_inspect: bool = field(default=True)

    @classmethod
    def parse(cls, monkey_str: str, divide_after_inspect: bool = True) -> 'Monkey':
        tokens = MONKEY_PATTERN.match(monkey_str).groups()  # type: ignore

        # Parse operation function; None is placeholder for current item value
        op_tokens = tokens[2].split()
        lhs = None if op_tokens[0] == 'old' else int(op_tokens[0])
        rhs = None if op_tokens[2] == 'old' else int(op_tokens[2])
        if op_tokens[1] == '+':

            def operator(x, y):
                return x + y

        if op_tokens[1] == '*':

            def operator(x, y):
                return x * y

        def operation(x: int):
            return operator(lhs or x, rhs or x)

        return cls(
            id=int(tokens[0]),
            items=[int(item.strip()) for item in tokens[1].split(',')],
            operation=operation,
            test_divisible=int(tokens[3]),
            next_true=int(tokens[4]),
            next_false=int(tokens[5]),
            divide_after_inspect=divide_after_inspect,
        )

    @property
    def items_str(self) -> str:
        return ', '.join([str(i) for i in self.items])

    def inspect_items(self) -> Iterator[tuple[int, int]]:
        for item in self.items:
            yield self.next_monkey(item)
            self.n_inspected += 1
        self.items = []

    def next_monkey(self, item: int) -> tuple[int, int]:
        item = self.operation(item)
        if self.divide_after_inspect:
            item = int(item / 3)
        else:
            item %= self.modulo

        if item % self.test_divisible == 0:
            return item, self.next_true
        else:
            return item, self.next_false


def run_rounds(data: str, n_rounds: int, divide_after_inspect: bool = True) -> MonkeyMap:
    monkeys = {
        m.id: m for m in [Monkey.parse(m, divide_after_inspect) for m in data.split('Monkey ') if m]
    }
    modulo = 1
    for m in monkeys.values():
        modulo *= m.test_divisible
    for m in monkeys.values():
        m.modulo = modulo

    def run_round():
        for monkey in monkeys.values():
            logger.debug(f'Turn: monkey {monkey.id}')
            for item, pass_to in monkey.inspect_items():
                recipient = monkeys[pass_to]
                recipient.items.append(item)
                logger.debug(f'  Passed item with value {item} to monkey {pass_to}')

    for i in range(n_rounds):
        run_round()
        logger.debug(f'Round {i}:')
        for monkey in monkeys.values():
            logger.debug(f'  Monkey {monkey.id}: {monkey.items_str}')

    return monkeys


def monkey_business(monkeys: MonkeyMap) -> int:
    sorted_monkeys = sorted(monkeys.values(), key=lambda m: m.n_inspected, reverse=True)
    return sorted_monkeys[0].n_inspected * sorted_monkeys[1].n_inspected


def solve(**kwargs) -> Solution:
    data = read_input(11, **kwargs)
    monkeys = run_rounds(data, 20, divide_after_inspect=True)
    answer_1 = monkey_business(monkeys)
    logger.info(f'Part 1: {answer_1}')

    monkeys = run_rounds(data, 10000, divide_after_inspect=False)
    answer_2 = monkey_business(monkeys)
    logger.info(f'Part 2: {answer_2}')
    return answer_1, answer_2
