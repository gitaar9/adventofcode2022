import fileinput


def calc_shape_score(shape):
    if shape == 'rock':
        return 1
    elif shape == 'paper':
        return 2
    elif shape == 'scissors':
        return 3
    raise ValueError('invalid shape')


def calc_match_points(opponent_shape, my_shape):
    if opponent_shape == my_shape:
        return 3
    elif opponent_shape == 'rock' and my_shape == 'scissors' or opponent_shape == 'paper' and my_shape == 'rock' or opponent_shape == 'scissors' and my_shape == 'paper':
        return 0
    else:
        return 6


def calculate_round_score(round):
    opponents_shape, my_shape = round
    return calc_shape_score(my_shape) + calc_match_points(opponents_shape, my_shape)


def parse_stdin():
    rounds = []
    opponent_conversion = {
        'A': 'rock',
        'B': 'paper',
        'C': 'scissors'
    }
    my_conversion = {
        'X': 'lose',
        'Y': 'draw',
        'Z': 'win'
    }

    for line in fileinput.input():
        opponents_play, my_play = line.strip().split()

        rounds.append((opponent_conversion[opponents_play], my_conversion[my_play]))
    return rounds


def what_should_i_play(input_pair):
    opponent_shape, required_output = input_pair
    if required_output == 'draw':
        return opponent_shape
    if required_output == 'win':
        if opponent_shape == 'rock':
            return 'paper'
        if opponent_shape == 'scissors':
            return 'rock'
        if opponent_shape == 'paper':
            return 'scissors'
    if required_output == 'lose':
        if opponent_shape == 'rock':
            return 'scissors'
        if opponent_shape == 'scissors':
            return 'paper'
        if opponent_shape == 'paper':
            return 'rock'


def main():
    rounds = parse_stdin()
    # total_points = sum(map(calculate_round_score, rounds))

    correct_shape = list(map(what_should_i_play, rounds))

    new_rounds = [(opponent_shape, my_shape) for (opponent_shape, _), my_shape in zip(rounds, correct_shape)]
    total_points = sum(map(calculate_round_score, new_rounds))
    print(total_points)


if __name__ == '__main__':
    main()
