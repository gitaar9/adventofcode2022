import fileinput
import string
from copy import deepcopy
from typing import List, Set
import numpy as np
import matplotlib.pyplot as plt
import bisect


def parse_stdin():
    lines = [list(line.strip()) for line in fileinput.input()]
    a = np.asarray(lines)
    start_y, start_x = np.where(a == 'S')
    end_y, end_x = np.where(a == 'E')
    a[start_y, start_x] = 'a'
    a[end_y, end_x] = 'z'
    to_int = lambda x: ord(x) - 97
    to_int = np.vectorize(to_int)
    a = to_int(a)
    print(a.shape)

    return a, (start_y[0], start_x[0]), (end_y[0], end_x[0])


def distance(loc, end):
    return abs(end[0] - loc[0]) + abs(end[1] - loc[1])

def get_possible_actions(location, map):
    height, width = map.shape
    location = np.asarray(location)
    current_height_value = map[location[0], location[1]]
    directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    possible_actions = []
    for dir in directions:
        new_location = location + dir
        y, x = new_location
        if x < 0 or y < 0 or y > (height - 1) or x > (width - 1):
            continue
        if map[new_location[0], new_location[1]] <= (current_height_value + 1):
            possible_actions.append(tuple(new_location))
    return possible_actions


def remove_duplicates(action_list):
    pass


def main():
    map, start, end = parse_stdin()
    start_value = 99999
    time_map = np.ones_like(map, dtype=int) * start_value
    # plt.imshow(map)
    # plt.show()

    start_locations = np.where(map == 0)
    start_locations = list(zip(*start_locations))
    action_list = [(start, distance(start, end), 0) for start in start_locations]
    explored_tiles = {start}
    action_idx = 0

    while len(action_list) > 0:
        action_list = sorted(action_list, key=lambda p: (p[1], p[2]), reverse=True)
        location, _, step_until_here = action_list.pop()
        new_actions = get_possible_actions(location, map)
        for action in new_actions:
            if (step_until_here + 1) < time_map[action[0], action[1]]:
                action_list.append((action, distance(action, end), step_until_here + 1))
                time_map[action[0], action[1]] = step_until_here + 1
        explored_tiles.add(location)
        # if time_map[end[0], end[1]] != start_value:
        #     break
        action_idx += 1

    time_map[time_map == start_value] = 0
    fig, axs = plt.subplots(2, 1)
    axs.flat[0].imshow(map)
    axs.flat[1].imshow(time_map)
    plt.title(time_map[end[0], end[1]])
    plt.show()

    print(map)
    print(start, end)
    print(time_map)

    print(time_map[end[0], end[1]])


if __name__ == '__main__':
    main()
