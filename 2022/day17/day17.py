import fileinput
import functools
import string
from copy import deepcopy
from dataclasses import dataclass
from typing import List, Set, Tuple
import numpy as np
import matplotlib.pyplot as plt
import bisect
from time import sleep

from tqdm import tqdm


GRID_HEIGHT = 400
ROCKS = [
    np.asarray([['#', '#', '#', '#']], dtype=str),
    np.asarray([['.', '#', '.'], ['#', '#', '#'], ['.', '#', '.']], dtype=str),
    np.asarray([['.', '.', '#'], ['.', '.', '#'], ['#', '#', '#']], dtype=str),
    np.asarray([['#'], ['#'], ['#'], ['#']], dtype=str),
    np.asarray([['#', '#'], ['#', '#']], dtype=str)
]


def parse_stdin():
    line = [line.strip() for line in fileinput.input()][0]
    return list(line)


def place_on_grid(rock_pos, rock, grid, fill_with='#'):
    rock_height, rock_width = rock.shape
    grid[rock_pos[1]:rock_pos[1] + rock_height, rock_pos[0]:rock_pos[0] + rock_width][(np.flip(rock, axis=0) == '#')] = fill_with  # (np.flip(grid_where_the_rock_is, axis=0) == '.') &


def print_grid(grid, falling_rock=None, falling_rock_pos=None):
    if falling_rock is not None:
        falling_rock = deepcopy(falling_rock)
        grid = deepcopy(grid)
        place_on_grid(falling_rock_pos, falling_rock, grid, fill_with='@')

        # grid[falling_rock_pos[1]:falling_rock_pos[1] + rock_height, falling_rock_pos[0]:falling_rock_pos[0] + rock_width] = falling_rock
    print('-------')
    if falling_rock_pos:
        print(falling_rock_pos)
    for idx, row in reversed(list(enumerate(grid))):
        print("".join(row) + str(idx))
    print('-------')
    print()


def to_right_is_blocked(new_rock, rock_pos, grid):
    y, x = np.where(np.flip(new_rock, 0) == '#')
    for coord in zip(x, y):
        coord = (coord[0] + rock_pos[0] + 1, coord[1] + rock_pos[1])
        if coord[0] >= grid.shape[1] or grid[coord[1], coord[0]] == '#':
            # print('Right is blocked!')
            return True
    return False


def to_left_is_blocked(new_rock, rock_pos, grid):
    y, x = np.where(np.flip(new_rock, 0) == '#')
    for coord in zip(x, y):
        coord = (coord[0] + rock_pos[0] - 1, coord[1] + rock_pos[1])
        if coord[0] == -1 or grid[coord[1], coord[0]] == '#':
            # print('Left is blocked!')

            return True
    return False


def is_supported(new_rock, rock_pos, grid):
    y, x = np.where(np.flip(new_rock, 0) == '#')
    # print([coord for coord in zip(x, y)])
    for coord in zip(x, y):
        coord = (coord[0] + rock_pos[0], coord[1] + rock_pos[1] - 1)
        if coord[1] == -1 or grid[coord[1], coord[0]] == '#':
            return True
    return False


def init_grid():
    grid = np.chararray((GRID_HEIGHT, 7))
    grid[:] = '.'
    return grid.astype(str)


def run_for_n_rocks(n_rocks, gas_jets, grid=None, highest_rock=0, jet_idx=0, removed_layers=0, previous_rock_index=0, solved_big_indexes=None, rock_start_index=0):
    step_size = len(gas_jets) * len(ROCKS)
    solved_big_indexes = solved_big_indexes or {}
    grid = init_grid() if grid is None else grid
    for rock_idx in range(rock_start_index, n_rocks):  # 1000000000000
        new_rock = ROCKS[rock_idx % len(ROCKS)]
        rock_height, rock_width = new_rock.shape
        rock_pos = [2, highest_rock + 3 - removed_layers]
        while True:
            jet_direction = gas_jets[jet_idx % len(gas_jets)]
            jet_idx += 1
            # Push the rock
            if jet_direction == '<':
                if not to_left_is_blocked(new_rock, rock_pos, grid):
                    rock_pos[0] -= 1
            else:
                if not to_right_is_blocked(new_rock, rock_pos, grid):
                    rock_pos[0] += 1
            # The rock falls
            if is_supported(new_rock, rock_pos, grid):
                place_on_grid(rock_pos, new_rock, grid, fill_with='#')
                highest_rock = max(rock_pos[1] + rock_height + removed_layers, highest_rock)
                for y_level in range(rock_pos[1], rock_pos[1] + rock_height):  # See if a level is fully blocked
                    if all(c == '#' for c in grid[y_level]):
                        new_grid = np.chararray((GRID_HEIGHT, 7))
                        new_grid[:] = '.'
                        new_grid = new_grid.astype(str)
                        new_grid[:GRID_HEIGHT - y_level, :] = grid[y_level:, :]
                        grid = new_grid
                        removed_layers += y_level
                        solved_big_indexes[previous_rock_index % step_size] = (deepcopy(grid), previous_rock_index, removed_layers, jet_idx % len(gas_jets), highest_rock, rock_idx)
                        previous_rock_index = rock_idx
                        if rock_idx % step_size in solved_big_indexes:
                            # print(f'It happened at {rock_idx} for {big_index}')
                            # print(solved_big_indexes[big_index])
                            # print(rock_idx % step_size, removed_layers, jet_idx % len(gas_jets))
                            # print(tuple(solved_big_indexes[big_index][0].flatten()) == tuple(grid.flatten()))
                            next_grid, next_previous_rock_index, next_removed_layers, next_jet_idx, next_highest_rock, next_rock_idx = solved_big_indexes[rock_idx % step_size]
                            print(f'We are at {n_rocks - (rock_idx + (next_rock_idx - next_previous_rock_index))} to go.')
                            return run_for_n_rocks(
                                n_rocks=n_rocks,
                                gas_jets=gas_jets,
                                grid=next_grid,
                                highest_rock=next_highest_rock,
                                jet_idx=next_jet_idx,
                                removed_layers=next_removed_layers,
                                previous_rock_index=next_rock_idx % step_size,
                                solved_big_indexes=solved_big_indexes,
                                rock_start_index=rock_idx + (next_rock_idx - next_previous_rock_index)
                            )
                break
            else:
                rock_pos[1] -= 1
    return grid, highest_rock, jet_idx, removed_layers


def main():
    import  sys
    # resource.setrlimit(resource.RLIMIT_STACK, (2 ** 29, -1))
    sys.setrecursionlimit(10 ** 6)

    after_n_rocks = 1000000000000  # 1000000000000  #
    gas_jets = parse_stdin()
    print(len(gas_jets))
    print(len(gas_jets) * len(ROCKS))
    earlier_seen_states = []
    step_size = len(gas_jets) * len(ROCKS)

    _, highest_rock, _, _ = run_for_n_rocks(after_n_rocks, gas_jets)
    print(highest_rock)

    exit()

    grid = init_grid()
    highest_rock = 0
    jet_idx = 0
    removed_layers = 0
    for epoch_id in tqdm(range(after_n_rocks // step_size)):
        grid, highest_rock, jet_idx, removed_layers = run_for_n_rocks(
            n_rocks=step_size,
            gas_jets=gas_jets,
            grid=grid,
            highest_rock=highest_rock,
            jet_idx=jet_idx,
            removed_layers=removed_layers
        )
        flat_state = tuple(grid.flatten())
        for earlier_state in earlier_seen_states:
            if flat_state == earlier_state:
                print(f'It happened at {epoch_id}')
        earlier_seen_states.append(flat_state)

    # Deal with leftovers
    grid, highest_rock, jet_idx, removed_layers = run_for_n_rocks(
        n_rocks=after_n_rocks % step_size,
        gas_jets=gas_jets,
        grid=grid,
        highest_rock=highest_rock,
        jet_idx=jet_idx,
        removed_layers=removed_layers
    )

    # print_grid(grid[:40, :])
    print(highest_rock)


if __name__ == '__main__':
    main()