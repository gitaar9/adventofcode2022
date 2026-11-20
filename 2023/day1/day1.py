import fileinput


def parse_stdin():
    return [line.strip() for line in fileinput.input()]


def replace_spelled_digits_by_digits(lines):
    digit_replacements = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9
    }
    all_lines = "\n".join(lines)
    for search, replace in digit_replacements.items():
        all_lines = all_lines.replace(search, search + str(replace) + search)
    return all_lines.split("\n")


def remove_non_digits(s):
    return [c for c in s if c.isdigit()]


def main():
    lines = parse_stdin()
    lines = replace_spelled_digits_by_digits(lines)
    # print(lines)
    only_digits = [remove_non_digits(line) for line in lines]
    combined_digits = [int(a[0] + a[-1]) for a in only_digits]
    print(sum(combined_digits))


if __name__ == '__main__':
    main()
