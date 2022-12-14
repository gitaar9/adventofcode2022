import fileinput
import functools
import math
import string
from copy import deepcopy
from typing import List, Set
import numpy as np
from tqdm import tqdm


class Monkey:
    def __init__(self, info):
        self.monkey_id = int(info[0][7])
        self.items = list(map(int, info[1].split(':')[-1].strip().split(', ')))
        self.operation = info[2].split(':')[-1].strip().split('=')[-1].strip()
        self.divisible_by_test = int(info[3].split()[-1])
        self.true_monkey = int(info[4].split()[-1])
        self.false_monkey = int(info[5].split()[-1])
        self.inspected_items_count = 0
        self.previous_worry_levels = {}
        self.big_divisor = 1

    def perform_operation(self, old):
        return int(eval(self.operation))

    def __repr__(self):
        return f"{self.monkey_id} {self.items}"

    def add_item(self, worry_level):
        self.items.append(worry_level)

    def turn(self, all_monkeys):
        for item in self.items:
            self.inspected_items_count += 1
            if item in self.previous_worry_levels:
                to, final_level = self.previous_worry_levels[item]
                all_monkeys[to].add_item(final_level)  # Throw the item
            else:
                worry_level = item
                worry_level = self.perform_operation(worry_level)  # Worry increase
                worry_level = worry_level % self.big_divisor  # Worry decreases
                if worry_level % self.divisible_by_test == 0:  # Check who we throw to
                    to_monkey = self.true_monkey
                else:
                    to_monkey = self.false_monkey
                all_monkeys[to_monkey].add_item(worry_level)  # Throw the item
                self.previous_worry_levels[item] = (to_monkey, worry_level)  # Cache the result
        self.items = []


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def parse_stdin():
    monkeys = []
    lines = [line.strip() for line in fileinput.input()]
    for info in chunks(lines, 7):
        monkeys.append(Monkey(info))
    return monkeys


def main():
    monkeys = parse_stdin()
    print(monkeys)
    print(monkeys[0].perform_operation(10))
    rounds = 10000
    big_divisor = math.prod(m.divisible_by_test for m in monkeys)
    for m in monkeys:
        m.big_divisor = big_divisor
    for _ in tqdm(range(rounds)):
        for m in monkeys:
            m.turn(monkeys)
    print("\n".join(map(str, monkeys)))
    print("\n".join(map(str, [m.inspected_items_count for m in monkeys])))

    most_active_monkeys = sorted([m.inspected_items_count for m in monkeys])[-2:]
    monkey_business = most_active_monkeys[0] * most_active_monkeys[1]
    print(monkey_business)


if __name__ == '__main__':
    main()
