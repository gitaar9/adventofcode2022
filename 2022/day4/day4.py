import fileinput
import string


def parse_stdin():
    elf_pairs = []

    for line in fileinput.input():
        elves = line.strip().split(',')

        elves = [set(range(int(elf.split('-')[0]), int(elf.split('-')[1]) + 1)) for elf in elves]

        elf_pairs.append(elves)

    return elf_pairs


def one_is_subset_of_other(elf_pairs):
    elf1, elf2 = elf_pairs
    return len(elf1.union(elf2)) == max(map(len, elf_pairs))


def have_overlap(elf_pairs):
    elf1, elf2 = elf_pairs
    return len(elf1.union(elf2)) != (len(elf1) + len(elf2))


def main():
    elf_pairs = parse_stdin()
    print(elf_pairs)
    print(sum(map(one_is_subset_of_other, elf_pairs)))
    print(sum(map(have_overlap, elf_pairs)))


if __name__ == '__main__':
    main()
