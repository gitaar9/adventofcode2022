import fileinput
import string


def item_to_priority(item):
    alphabet = list(string.ascii_lowercase)
    alphabet += [letter.upper() for letter in alphabet]
    conversion_dict = {letter: idx + 1 for idx, letter in enumerate(alphabet)}
    return conversion_dict[item]


def parse_stdin():
    bags = []

    for line in fileinput.input():
        line = line.strip()
        first_compartment = line[:len(line) // 2]
        second_compartment = line[len(line) // 2:]
        bags.append((first_compartment, second_compartment))

    return bags


def find_common_item(bag):
    first_compartment, second_compartment = bag
    for item in first_compartment:
        if item in second_compartment:
            return item
    raise RuntimeError('No common item in bag')


def find_common_item_in_group(group):
    group = [first_compartment + second_compartment for first_compartment, second_compartment in group]
    elf1, elf2, elf3 = group
    return list(set(elf1) & set(elf2) & set(elf3))[0]


def main():
    bags = parse_stdin()
    common_items = map(find_common_item, bags)
    priority_sum = sum(map(item_to_priority, common_items))
    print(priority_sum)
    groups = [bags[group_start_idx:group_start_idx + 3] for group_start_idx in range(0, len(bags), 3)]
    print(sum(map(item_to_priority, map(find_common_item_in_group, groups))))


if __name__ == '__main__':
    main()
