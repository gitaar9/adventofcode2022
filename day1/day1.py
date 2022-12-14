import fileinput


def parse_stdin():
    elves = []
    current_elf = []
    for line in fileinput.input():
        line = line.strip()
        if line:
            current_elf.append(int(line))
        else:
            elves.append(current_elf)
            current_elf = []
    if current_elf:
        elves.append(current_elf)
    return elves


def main():
    elves = parse_stdin()
    summed_calories = map(sum, elves)
    print(max(summed_calories))
    print(sum(sorted(summed_calories)[-3:]))


if __name__ == '__main__':
    main()
