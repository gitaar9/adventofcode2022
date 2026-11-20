import fileinput
import itertools
from dataclasses import dataclass
from math import prod
from typing import Dict, List

import numpy as np


@dataclass
class Number:
    value: int
    row_idx: int
    start_col_idx: int
    end_col_idx: int

    def _direct_neighbours_bb(self):
        x0 = max(0, self.start_col_idx - 1)
        y0 = max(0, self.row_idx - 1)
        x1 = self.end_col_idx + 1
        y1 = self.row_idx + 2
        return x0, y0, x1, y1

    def _direct_neighbours(self, map: np.ndarray):
        x0, y0, x1, y1 = self._direct_neighbours_bb()
        return map[y0:y1, x0:x1]

    def is_adjacent_to_symbol(self, map: np.ndarray):
        direct_neighbours = self._direct_neighbours(map)
        not_digit_and_not_period = ~np.core.defchararray.isdigit(direct_neighbours) & (direct_neighbours != '.')
        return np.any(not_digit_and_not_period)

    def find_adjacent_candidate_gears(self, map: np.ndarray):
        x0, y0, _, _ = self._direct_neighbours_bb()
        ys, xs = np.where(self._direct_neighbours(map) == '*')
        xs += x0
        ys += y0
        coords = list(zip(xs, ys))
        return [(coord, self.value) for coord in coords]


def parse_stdin():
    return [line.strip() for line in fileinput.input()]


def parse_numbers(arr: np.ndarray):
    numbers: List[Number] = []
    for row_idx, row in enumerate(arr):
        current_number = ""
        start_col_idx = 0
        for col_idx, c in enumerate(row):
            if c.isdigit():
                if current_number == "":
                    start_col_idx = col_idx
                current_number += c
            else:
                if current_number != "":
                    numbers.append(Number(int(current_number), row_idx, start_col_idx, col_idx))
                    current_number = ""
                start_col_idx = col_idx
        if current_number != "":
            numbers.append(Number(int(current_number), row_idx, start_col_idx, len(row)))

    return numbers


def main():
    lines = parse_stdin()
    map = np.array([list(line) for line in lines])
    numbers = parse_numbers(map)

    print(sum(number.value for number in numbers if number.is_adjacent_to_symbol(map)))

    candidate_gears = {}
    for number in numbers:
        for coord, value in number.find_adjacent_candidate_gears(map):
            if coord in candidate_gears:
                candidate_gears[coord].append(value)
            else:
                candidate_gears[coord] = [value]

    validated_gears = {coord: values for coord, values in candidate_gears.items() if len(values) == 2}
    print(sum(value_1 * value_2 for value_1, value_2 in validated_gears.values()))



if __name__ == '__main__':
    main()
