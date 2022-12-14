import fileinput
import string
from copy import deepcopy
from typing import List, Set
import numpy as np


class KnotSimulator:
    def __init__(self):
        self.amount_of_tails = 9
        self.head_position = (0, 0)
        self.tail_positions = [(0, 0)] * self.amount_of_tails

        self.prev_tail_locations = {self.tail_positions[-1]}

    def complete_instruction(self, direction, times):
        for _ in range(times):
            self.move_head(direction)

    def move_head(self, direction):
        print(direction)
        self.head_position = list(self.head_position)
        if direction == 'R':
            self.head_position[0] += 1
        elif direction == 'L':
            self.head_position[0] -= 1
        elif direction == 'U':
            self.head_position[1] += 1
        elif direction == 'D':
            self.head_position[1] -= 1
        else:
            raise ValueError('Invalid instruction')
        self.head_position = tuple(self.head_position)
        self.move_tails()

    def move_tails(self):
        for tail_idx in range(self.amount_of_tails):
            if tail_idx == 0:
                temp_head = self.head_position
            else:
                temp_head = self.tail_positions[tail_idx - 1]
            self.move_tail(temp_head, tail_idx)
        self.prev_tail_locations.add(self.tail_positions[-1])

    @staticmethod
    def calc_new_tail_pos(old_tail_pos, x_diff, y_diff):
        new_tail_pos = list(old_tail_pos)

        if abs(x_diff) <= 1 and abs(y_diff) <= 1:
            pass
        elif abs(x_diff) == 2 and y_diff == 0:
            new_tail_pos[0] += 1 if x_diff > 0 else -1
        elif x_diff == 0 and abs(y_diff) == 2:
            new_tail_pos[1] += 1 if y_diff > 0 else -1
        elif abs(x_diff) != 0 and abs(y_diff) != 0:
            new_tail_pos[0] += 1 if x_diff > 0 else -1
            new_tail_pos[1] += 1 if y_diff > 0 else -1

        return tuple(new_tail_pos)

    def move_tail(self, head_pos, tail_idx):
        x_diff = head_pos[0] - self.tail_positions[tail_idx][0]
        y_diff = head_pos[1] - self.tail_positions[tail_idx][1]
        assert (0 <= abs(x_diff) < 3)
        assert (0 <= abs(y_diff) < 3)

        self.tail_positions[tail_idx] = self.calc_new_tail_pos(self.tail_positions[tail_idx], x_diff, y_diff)

    @staticmethod
    def calc_new_tail_pos_old(old_tail_pos, x_diff, y_diff):
        new_tail_pos = list(old_tail_pos)

        if abs(x_diff) == 2:
            if y_diff == 0:
                new_tail_pos[0] += x_diff // 2
            else:
                new_tail_pos[0] += x_diff // 2
                new_tail_pos[1] += y_diff
        if abs(y_diff) == 2:
            if x_diff == 0:
                new_tail_pos[1] += y_diff // 2
            else:
                new_tail_pos[1] += y_diff // 2
                new_tail_pos[0] += x_diff

        return tuple(new_tail_pos)

def parse_stdin():
    instructions = []
    for line in fileinput.input():
        ins = line.strip().split()
        instructions.append((ins[0], int(ins[1])))

    return instructions


def main():
    instructions = parse_stdin()
    ks = KnotSimulator()
    for instruction in instructions:
        ks.complete_instruction(*instruction)
    print(ks.prev_tail_locations)
    print(len(ks.prev_tail_locations))
    # map = np.zeros((5, 5))
    # for x, y in ks.prev_tail_locations:
    #     map[y, x] = 1
    # print(map)


if __name__ == '__main__':
    main()
