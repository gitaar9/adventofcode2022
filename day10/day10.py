import fileinput
import string
from copy import deepcopy
from typing import List, Set
import numpy as np


class CRT:
    def __init__(self):
        self.width = 40
        self.height = 6
        self.screen = np.chararray((6, 40), unicode=True)
        self.screen[:] = '.'

    def show(self):
        for row in self.screen:
            s = ''
            for c in row:
                s += ' ' if c == '.' else '#'
            print(s)

    def draw(self, cycle, value_x):
        location = (cycle - 1) % (self.width * self.height)
        column = location % self.width
        row = location // self.width
        sprite_middle = value_x % self.width

        print(location, sprite_middle)
        if abs(column - sprite_middle) <= 1:
            assert row < self.height
            assert column < self.width
            self.screen[row, column] = '#'

"""PZGPKPEB"""
class CPU:
    def __init__(self):
        self.registerX = 1
        self.cycle_count = 1
        self.verbose = True
        self.execution_list = []
        self.signal_strength = 0
        self.crt = CRT()

    def add_x(self, arg):
        self.registerX += arg

    def execute(self, instructions):
        instructions = list(reversed(instructions))
        current_instruction = None
        while len(instructions) > 0:
            self.crt.draw(self.cycle_count, self.registerX)
            if current_instruction is None:
                current_instruction = instructions.pop()
                command, argument = current_instruction
                if command == 'noop':
                    current_instruction = None
            else:
                self.add_x(argument)
                current_instruction = None

            self.cycle_count += 1
            if (self.cycle_count + 20) % 40 == 0:
                print(f'Local signal strength: {self.cycle_count * self.registerX}')
                self.signal_strength += self.cycle_count * self.registerX
            print(f'At {self.cycle_count} X: {self.registerX}')
        if current_instruction is not None:
            self.crt.draw(self.cycle_count, self.registerX)
            self.add_x(argument)
            self.cycle_count += 1
            print(f'At {self.cycle_count} X: {self.registerX}')
        self.crt.draw(self.cycle_count, self.registerX)


def parse_stdin():
    instructions = []
    for line in fileinput.input():
        s = line.strip().split()
        if len(s) == 1:
            instructions.append((s[0], None))
        else:
            command, argument = s
            instructions.append((command, int(argument)))

    return instructions


def main():
    instructions = parse_stdin()
    c = CPU()
    c.execute(instructions)
    print(c.signal_strength)
    c.crt.show()

if __name__ == '__main__':
    main()
