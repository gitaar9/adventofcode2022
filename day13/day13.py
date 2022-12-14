import fileinput
import functools
import string
from copy import deepcopy
from typing import List, Set
import numpy as np
import matplotlib.pyplot as plt
import bisect


def parse_stdin():
    lines = [line.strip() for line in fileinput.input()]
    pairs_of_packets = []
    for idx in range(0, len(lines), 3):
        print(idx, lines[idx])
        first_packet = eval(lines[idx])
        second_packet = eval(lines[idx + 1])
        pairs_of_packets.append((first_packet, second_packet))
    return pairs_of_packets


def right_order(left, right):
    left = deepcopy(left)
    right = deepcopy(right)
    if len(left) == 0 and len(right) == 0:
        return None
    try:  # Running out of left side is fine
        left_item = left[0]
        del left[0]
    except IndexError:
        return 1
    try:  # If we run out of right side they are not in order
        right_item = right[0]
        del right[0]
    except IndexError:
        return -1

    if isinstance(left_item, int) and isinstance(right_item, int):
        if left_item == right_item:
            return right_order(left, right)  # Go next item
        else:
            return 1 if left_item < right_item else -1  # Return right order or not

    # Make sure we have two lists
    if not isinstance(left_item, list):
        assert isinstance(left_item, int)
        left_item = [left_item]
    if not isinstance(right_item, list):
        assert isinstance(right_item, int)
        right_item = [right_item]
    # Compare the lists
    result_of_list_comparison = right_order(left_item, right_item)
    if result_of_list_comparison is None:
        return right_order(left, right)  # Go next item
    else:
        return result_of_list_comparison  # Return right order or not




def main():
    pairs_of_packets = parse_stdin()
    # idx_of_right_order = [idx + 1 for idx, (p1, p2) in enumerate(pairs_of_packets) if right_order(p1, p2)]
    # print(sum(idx_of_right_order))
    print('\n' * 3)
    packets = []
    for p1, p2 in pairs_of_packets:
        packets.append(p1)
        packets.append(p2)
    packets.append([[2]])
    packets.append([[6]])
    l = list(sorted(packets, key=functools.cmp_to_key(right_order), reverse=True))
    for p in l:
        print(p)
    # between 4359 and 6520
    print(l.index([[2]]))
    print(l.index([[6]]))
    print('\n', (l.index([[2]]) + 1) * (l.index([[6]]) + 1))


if __name__ == '__main__':
    main()
