import fileinput
import string


def parse_stdin():
    instructions_started = False
    layers = []
    instructions = []

    for line in fileinput.input():
        line = line.rstrip()
        if instructions_started:
            instructions.append(line)
            continue
        if not line:
            instructions_started = True
            continue
        idx = 1
        layer = []
        while idx < len(line):
            layer.append(line[idx])
            idx += 4
        if all(l.isnumeric() for l in layer):
            continue
        layers.append(layer)
    amount_of_stacks = max(map(len, layers))
    stacks = []
    for _ in range(amount_of_stacks):
        stacks.append([])

    for layer in reversed(layers):
        for stack_idx, item in enumerate(layer):
            if item != ' ':
                stacks[stack_idx].append(item)
    instructions = [i.split() for i in instructions]
    instructions = [(int(i[1]), int(i[3]), int(i[5])) for i in instructions]

    return stacks, instructions


def apply_instruction(stacks, instruction):
    amount, from_stack, to_stack = instruction
    picked_up = []
    for _ in range(amount):
        picked_up.append(stacks[from_stack - 1].pop())
    for _ in range(amount):
        stacks[to_stack - 1].append(picked_up.pop())
    # stacks[to_stack - 1].extend(picked_up)


def main():
    stacks, instructions = parse_stdin()
    for instruction in instructions:
        print(stacks)
        apply_instruction(stacks, instruction)
    print(''.join([stack.pop() for stack in stacks]))
    # print(stacks, instructions)


if __name__ == '__main__':
    main()
