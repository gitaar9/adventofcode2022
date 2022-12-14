import fileinput
import string


def parse_stdin():
    for line in fileinput.input():
        s = line.strip()
    return s


def find_start_of_packet(stream):
    for i in range(3, len(stream)):
        if len({stream[i], stream[i - 1], stream[i - 2], stream[i - 3]}) == 4:
            return i + 1
    raise ValueError('No start of packet')


def find_start_of_message(stream):
    different_characters = 14
    for i in range(different_characters - 1, len(stream)):
        chars = {stream[i - relative_char_idx] for relative_char_idx in range(different_characters)}
        if len(chars) == different_characters:
            return i + 1
    raise ValueError('No start of message')


def main():
    datastream = parse_stdin()
    print(find_start_of_packet(datastream))
    print(find_start_of_message(datastream))
    # print(stacks, instructions)


if __name__ == '__main__':
    main()
