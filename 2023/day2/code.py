import fileinput
import itertools
from dataclasses import dataclass
from math import prod
from typing import Dict, List


def set_is_possible(set, max_cubes_per_color):
    return all(amount <= max_cubes_per_color[color] for color, amount in set.items())


@dataclass
class Game:
    game_idx: int
    sets: List[Dict[str, int]]

    def is_possible(self, max_cubes_per_color: Dict[str, int]):
        return all(set_is_possible(s, max_cubes_per_color) for s in self.sets)

    def min_cubes_per_color(self):
        min_cubes_per_color = {}
        for set in self.sets:
            for color, amount in set.items():
                if color in min_cubes_per_color:
                    min_cubes_per_color[color] = max(amount, min_cubes_per_color[color])
                else:
                    min_cubes_per_color[color] = amount
        return min_cubes_per_color

    def power(self):
        return prod(self.min_cubes_per_color().values())


def parse_stdin():
    return [line.strip() for line in fileinput.input()]


def parse_games(lines):
    games = []
    for line in lines:
        header, sets = line.split(': ')
        game_idx = int(header.split(' ')[-1])
        parsed_sets = []
        sets = sets.split('; ')
        for set in sets:
            parsed_sets.append({})
            for cube_count in set.split(', '):
                amount, color = cube_count.split(' ')
                parsed_sets[-1][color] = int(amount)
        games.append(Game(game_idx, parsed_sets))
    return games


def main():
    max_cubes_per_color = {
        'red': 12,
        'green': 13,
        'blue': 14
    }
    lines = parse_stdin()
    games = parse_games(lines)

    possible_games = [g for g in games if g.is_possible(max_cubes_per_color)]
    print(sum(g.game_idx for g in possible_games))

    print([(g.min_cubes_per_color(), g.power()) for g in games])

    print(sum(g.power() for g in games))


if __name__ == '__main__':
    main()
