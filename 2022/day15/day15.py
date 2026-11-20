import fileinput
import functools
import string
from copy import deepcopy
from typing import List, Set, Tuple
import numpy as np
import matplotlib.pyplot as plt
import bisect

from tqdm import tqdm


def print_grid(grid):
    for row in grid:
        print("".join(row))


def manhattan_distance(t1, t2):
    return abs(t1[0] - t2[0]) + abs(t1[1] - t2[1])


def with_a_set(sensor_x, sensor_y, distances, square_size):
    my_set = set()
    for sx, sy, distance in tqdm(list(zip(sensor_x, sensor_y, distances))):
        for x in range(max(sx - (distance), 0), min(sx + (distance) + 1, square_size)):
            x_dis = abs(sx - x)
            y_coords = range(max(sy - (distance - x_dis), 0), min(sy + (distance - x_dis) + 1, square_size))
            for y in y_coords:
                my_set.add((x, y))
            # for y in range(max(sy - (distance - x_dis), 0), min(sy + (distance - x_dis) + 1, square_size)):
            #     if abs(sx - x) + abs(sy - y) <= distance:
            #
            #     else:
            #         print("Does this even happen?")
        # break
    my_set = set(my_set)
    print(len(my_set))
    beacon_coord = None
    break_everywhere = False
    for x in range(square_size):
        for y in range(square_size):
            if (x, y) not in my_set:
                beacon_coord = (x, y)
                print(beacon_coord)
        #         break_everywhere = True
        #         break
        # if break_everywhere:
        #     break
    print(beacon_coord)
    print(beacon_coord[0] * 4000000 + beacon_coord[1])


def merge_column_infos(column_infos):
    for column_idx in range(len(column_infos)):
        last_column_info_length = -1
        while len(column_infos[column_idx]) != last_column_info_length:
            last_column_info_length = len(column_infos[column_idx])
            column_infos[column_idx] = sorted(column_infos[column_idx])
            new_ranges = [column_infos[column_idx][0]]
            prev_i = 0
            for i in range(1, last_column_info_length):
                prev_start, prev_end = new_ranges[prev_i]
                start, end = column_infos[column_idx][i]
                if prev_end >= end:  # This part is already covered by previous range
                    continue
                if prev_end >= start:
                    new_ranges[prev_i] = (prev_start, end)
                    continue
                new_ranges.append((start, end))
                prev_i += 1
            column_infos[column_idx] = new_ranges

    return column_infos


def main():
    lines = [line.strip() for line in fileinput.input()]

    sensor_x = np.array([
        int(line.split("x=")[1].split(",")[0]) for line in lines
    ])
    sensor_y = np.array([
        int(line.split("y=")[1].split(":")[0]) for line in lines
    ])
    beacon_x = np.array([
        int(line.split("x=")[2].split(",")[0]) for line in lines
    ])
    beacon_y = np.array([
        int(line.split("y=")[2]) for line in lines
    ])

    min_x = min(np.concatenate((sensor_x, beacon_x)))
    min_y = min(np.concatenate((sensor_y, beacon_y)))
    max_x = max(np.concatenate((sensor_x, beacon_x)))
    max_y = max(np.concatenate((sensor_y, beacon_y)))

    # sensor_x -= min_x
    # beacon_x -= min_x
    # sensor_y -= min_y
    # beacon_y -= min_y

    # grid = np.chararray((max_y - min_y + 1, max_x - min_x + 1))
    # grid[:] = '.'
    # grid = grid.astype(str)
    # grid[beacon_y, beacon_x] = 'B'
    # grid[sensor_y, sensor_x] = 'S'
    # print_grid(grid)

    distances = [
        abs(sx - bx) + abs(sy - by)
        for sx, sy, bx, by in zip(sensor_x, sensor_y, beacon_x, beacon_y)
    ]
    print(distances)
    beacon_coords = set(zip(beacon_x, beacon_y))

    square_size = 4000000 # 20
    # with_a_set(sensor_x, sensor_y, distances, square_size)
    column_infos = []
    for _ in range(square_size):
        column_infos.append([])

    for sx, sy, distance in tqdm(list(zip(sensor_x, sensor_y, distances))):
        for x in range(max(sx - (distance), 0), min(sx + (distance) + 1, square_size)):
            x_dis = abs(sx - x)
            min_y, max_y = max(sy - (distance - x_dis), 0), min(sy + (distance - x_dis) + 1, square_size)
            column_infos[x].append((min_y, max_y))
    column_infos = merge_column_infos(column_infos)

    for column_idx, column in enumerate(column_infos):
        if len(column) > 1:

            print(column_idx, column)
            (_, y), (_, _) = column
            print(column_idx * 4000000 + y)
    # print(beacon_coord[0] * 4000000 + beacon_coord[1])

    # print(len(my_set))
    # my_set_filtered = [
    #     (x, y)
    #     for x, y in my_set
    #     if 0 <= x < grid.shape[1] and 0 <= y < grid.shape[0]
    # ]
    #
    # for x, y in my_set_filtered:
    #     if grid[y, x] == ".":
    #         grid[y, x] = "#"
    #
    # print_grid(grid)


if __name__ == '__main__':
    main()
