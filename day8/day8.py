import fileinput
import string
from copy import deepcopy
from typing import List, Set
import numpy as np


def parse_stdin():
    arrays = []
    for line in fileinput.input():
        s = line.strip()
        arrays.append(list(s))

    return np.asarray(arrays, dtype=np.uint32)


def visible_trees(map):
    height, width = map.shape
    visible_points = np.zeros_like(map)

    # # Draw a outline
    # maxes_from_left = np.argmax(map, axis=1)
    # for row, column in zip(range(len(maxes_from_left)), maxes_from_left):
    #     visible_points[row, column] = 1
    #
    # maxes_from_top = np.argmax(map, axis=0)
    # for row, column in zip(maxes_from_top, range(len(maxes_from_top))):
    #     visible_points[row, column] = 1
    #
    # flipped_map = np.flip(map, 1)
    # # print(flipped_map)
    # maxes_from_right = np.argmax(flipped_map, axis=1)
    # maxes_from_right = (len(maxes_from_right) - 1) - maxes_from_right
    # for row, column in zip(range(len(maxes_from_right)), maxes_from_right):
    #     visible_points[row, column] = 1
    #
    # flipped_map = np.flip(map, 0)
    # maxes_from_bottom = np.argmax(flipped_map, axis=0)
    # maxes_from_bottom = (len(maxes_from_bottom) - 1) - maxes_from_bottom
    # for row, column in zip(maxes_from_bottom, range(len(maxes_from_bottom))):
    #     visible_points[row, column] = 1

    # Fill everything outside the outline
    for row in range(height):
        max_height = -1
        for idx in range(width):
            if map[row, idx] > max_height:
                visible_points[row, idx] = 1
                max_height = map[row, idx]

    for row in range(height):
        max_height = -1
        for idx in reversed(range(width)):
            if map[row, idx] > max_height:
                visible_points[row, idx] = 1
                max_height = map[row, idx]

    for column in range(width):
        max_height = -1
        for idx in range(height):
            if map[idx, column] > max_height:
                visible_points[idx, column] = 1
                max_height = map[idx, column]

    for column in range(width):
        max_height = -1
        for idx in reversed(range(height)):
            if map[idx, column] > max_height:
                visible_points[idx, column] = 1
                max_height = map[idx, column]

    return visible_points


def calculate_scenic_score(map, location):
    height, width = map.shape
    x, y = location
    location_height = map[y, x]

    trees_visible_to_left = 0
    temp_x = x - 1
    # print('to_left')
    while temp_x >= 0:
        trees_visible_to_left += 1
        # print(f"({temp_x}, {y}), {map[y, temp_x]}")
        if map[y, temp_x] >= location_height:
            break
        temp_x -= 1

    trees_visible_to_right = 0
    temp_x = x + 1
    # print('to_right')
    while temp_x < width:
        # print(f"({temp_x}, {y}), {map[y, temp_x]}")
        trees_visible_to_right += 1
        if map[y, temp_x] >= location_height:
            break
        temp_x += 1

    trees_visible_to_bottom = 0
    temp_y = y - 1
    while temp_y >= 0:
        trees_visible_to_bottom += 1
        if map[temp_y, x] >= location_height:
            break
        temp_y -= 1

    trees_visible_to_top = 0
    temp_y = y + 1
    while temp_y < height:
        trees_visible_to_top += 1
        if map[temp_y, x] >= location_height:
            break
        temp_y += 1
    # print(location_height)
    # print(trees_visible_to_top, trees_visible_to_left, trees_visible_to_bottom, trees_visible_to_right)
    return trees_visible_to_left * trees_visible_to_right * trees_visible_to_top * trees_visible_to_bottom


def main():
    map = parse_stdin()
    visible_points = visible_trees(map)
    print(np.sum(visible_points))

    print(map)
    print(calculate_scenic_score(map, (2, 3)))
    scenic_scores = np.zeros_like(map)
    height, width = map.shape
    print(f"Shape= ({map.shape})")
    for i in range(height):
        for j in range(width):
            scenic_scores[j, i] = calculate_scenic_score(map, (i, j))
    print(scenic_scores)
    print(np.max(scenic_scores))


if __name__ == '__main__':
    main()
