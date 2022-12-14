import fileinput
import functools
import string
from copy import deepcopy
from typing import List, Set, Tuple
import numpy as np
import matplotlib.pyplot as plt
import bisect


def parse_stdin():
    rock_formation_points = [line.strip().split(' -> ') for line in fileinput.input()]
    rock_formation_points = [[tuple(map(int, p.split(','))) for p in line] for line in rock_formation_points]

    return rock_formation_points


def show_depth_map(cave):
    for depth in range(10):
        print(f"{depth} {''.join(cave[depth, :])}")
    print()


def draw_rock_formation(cave, rock_formation_points):
    for rock_formation in rock_formation_points:
        for (start_x, start_depth), (end_x, end_depth) in zip(rock_formation, rock_formation[1:]):
            if start_x == end_x:
                for depth in range(start_depth if start_depth < end_depth else end_depth, start_depth + 1 if start_depth > end_depth else end_depth + 1):
                    cave[depth, start_x] = '#'
            elif start_depth == end_depth:
                for x in range(start_x if start_x < end_x else end_x, start_x + 1 if start_x > end_x else end_x + 1):
                    cave[start_depth, x] = '#'

    return cave


def add_one_sand_unit(cave: np.ndarray, sand_pours_from):
    new_sand_unit = sand_pours_from
    sand_is_stable = False
    while not sand_is_stable:
        sand_is_stable = True
        sand_unit_x, sand_unit_depth = new_sand_unit
        if cave[sand_unit_depth + 1, sand_unit_x] == '.':
            new_sand_unit = (sand_unit_x, sand_unit_depth + 1)
            sand_is_stable = False
            continue
        elif cave[sand_unit_depth + 1, sand_unit_x - 1] == '.':
            new_sand_unit = (sand_unit_x - 1, sand_unit_depth + 1)
            sand_is_stable = False
            continue
        elif cave[sand_unit_depth + 1, sand_unit_x + 1] == '.':
            new_sand_unit = (sand_unit_x + 1, sand_unit_depth + 1)
            sand_is_stable = False
            continue
    return new_sand_unit


def main():
    sand_pours_from = (500, 0)
    rock_formation_points = parse_stdin()

    # Init the cave
    cave = np.chararray((200, 2000), unicode=True)
    cave[:] = '.'
    cave[sand_pours_from[1], sand_pours_from[0]] = '+'
    cave = draw_rock_formation(cave, rock_formation_points)
    lowest_y = max([max([point[1] for point in rock_formation]) for rock_formation in rock_formation_points])
    print(f"Lowest point is at : {lowest_y}")
    cave[lowest_y + 2, :] = '#'

    show_depth_map(cave[0:10, 494:504])
    while cave[sand_pours_from[1], sand_pours_from[0]] == '+':
        try:
            new_sand_x, new_sand_depth = add_one_sand_unit(cave, sand_pours_from)
        except IndexError:
            break
        cave[new_sand_depth, new_sand_x] = 'O'
        show_depth_map(cave[0:10, 494:504])
    print(np.sum(cave == 'O'))


if __name__ == '__main__':
    main()
