import fileinput
import string
from copy import deepcopy
from typing import List, Set


class Directory:
    def __init__(self, directory_stack, listing=None):
        self.location: List[str] = deepcopy(directory_stack)
        self.dirs: Set[Directory] = set()
        self.files: Set[tuple] = set()
        self._size = None
        if listing:
            self.parse_listing(listing)

    @property
    def size(self):
        if self._size is not None:
            return self._size
        size = 0
        for file in self.files:
            size += file[0]
        for dir in self.dirs:
            size += dir.size

        self._size = size  # Cache the size
        return size

    @property
    def name(self):
        return self.location[-1]

    def add_listing(self, listing):
        for line in listing:
            if line[0] == 'dir':
                self.dirs.add(Directory(self.location + [line[1]]))
            else:
                self.files.add((int(line[0]), line[1]))

    def find_dir(self, directory_stack):
        if directory_stack == self.location:
            return self
        for directory in self.dirs:
            ret = directory.find_dir(directory_stack)
            if ret:
                return ret
        return None

    def all_dirs_inside(self):
        all_dirs = [self]
        for directory in self.dirs:
            all_dirs.extend(directory.all_dirs_inside())
        return all_dirs

    def dirs_smaller_than(self, value=100000):
        return [d for d in self.all_dirs_inside() if d.size <= value]

    def __repr__(self):
        return f'{"/".join(self.location)}\n\t{self.dirs}\n\t{self.files}'


def parse_stdin():
    directory_stack = ['/']
    root_dir = Directory(directory_stack)
    listing_started = False
    listed = []
    for line in fileinput.input():
        line = line.strip().split()
        if line[0] == '$':  # It's a command
            if listing_started:
                root_dir.find_dir(directory_stack).add_listing(listed)
                listing_started = False
                listed = []
            command = line[1]
            if command == 'ls':
                listing_started = True
            elif command == 'cd':
                argument = line[2]
                if argument == '..':
                    directory_stack.pop()
                elif argument == '/':
                    directory_stack = ['/']
                else:
                    directory_stack.append(argument)
        else:  # It's files or directories being listed
            listed.append(line)
    if listing_started:
        root_dir.find_dir(directory_stack).add_listing(listed)

    return root_dir


def main():
    root_dir = parse_stdin()
    print(root_dir)
    print(root_dir.size)
    print([d.name for d in root_dir.all_dirs_inside()])
    big_enough = root_dir.dirs_smaller_than()
    print(sum(d.size for d in big_enough))
    print()

    used_memory = root_dir.size
    unused_memory = 70000000 - root_dir.size
    needed_to_delete = 30000000 - unused_memory
    print(needed_to_delete)
    dir_sizes = sorted([(d.size) for d in root_dir.all_dirs_inside()])
    for s in dir_sizes:
        if s > needed_to_delete:
            print(s)
            break


if __name__ == '__main__':
    main()
