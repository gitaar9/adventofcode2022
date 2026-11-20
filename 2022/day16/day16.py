import fileinput
import functools
import string
from copy import deepcopy
from dataclasses import dataclass
from typing import List, Set, Tuple
import numpy as np
import matplotlib.pyplot as plt
import bisect
from time import sleep


START_TIME = 26
IDX_TO_NAME = None
DISTANCE_MATRIX = None


@dataclass
class State:
    locations: List[int]
    opened_valves: list
    released_pressure: int
    time_left: int
    story: List[str]
    _cached_potential: int = None

    def valve_in_current_room_can_be_opened(self, agent_idx, flow_rates: np.ndarray):
        return not self.opened_valves[self.locations[agent_idx]] and flow_rates[self.locations[agent_idx]] > 0

    def pressure_per_time(self):
        if START_TIME - self.time_left == 0:
            return 0
        return self.released_pressure / (START_TIME - self.time_left) + self.time_left * 5 #* DISTANCE_MATRIX[self.locations[0], self.locations[1]]

    def pressure_per_minute(self, flow_rates: np.ndarray):
        return np.sum(flow_rates[self.opened_valves])


def parse_stdin():
    lines = [line.strip() for line in fileinput.input()]
    valve_names = []
    flow_rates = []
    tunnels_to = []
    for line in lines:
        valve_info, tunnel_info = line.split(';')
        valve_names.append(valve_info.split()[1])
        flow_rates.append(int(valve_info.split('=')[1]))
        exits = tunnel_info.split()[4:]
        tunnels_to.append([e.replace(',', '') for e in exits])
    return valve_names, flow_rates, tunnels_to


def list_open_valves(s: State):
    return [IDX_TO_NAME[i] for i, b in enumerate(s.opened_valves) if b]


def is_better_than_existing_states(new_state: State, states: List[State]):
    for old_state in states:
        if old_state.locations[0] == new_state.locations[0] and old_state.locations[1] == new_state.locations[1] and all(v1 == v2 for v1, v2 in zip(new_state.opened_valves, old_state.opened_valves)):
            if new_state.released_pressure <= old_state.released_pressure and new_state.time_left <= old_state.time_left:
                return False
    return True


def compute_distance_matrix(valve_names, tunnels_to):
    global DISTANCE_MATRIX
    DISTANCE_MATRIX = np.ones((len(valve_names), len(valve_names)), dtype=int) * -1  # This is key

    for (x, y) in zip(range(len(valve_names)), range(len(valve_names))):
        DISTANCE_MATRIX[x, y] = 0
    while -1 in DISTANCE_MATRIX:
        for start in valve_names:
            for destination in valve_names:
                if DISTANCE_MATRIX[start, destination] == -1:
                    if destination in tunnels_to[start]:
                        DISTANCE_MATRIX[start, destination] = 1
                    for in_between in tunnels_to[start]:
                        if DISTANCE_MATRIX[in_between, destination] != -1:
                            DISTANCE_MATRIX[start, destination] = DISTANCE_MATRIX[in_between, destination] + 1


def main():
    valve_names, flow_rates, tunnels_to = parse_stdin()
    name_to_idx = {name: idx for idx, name in enumerate(valve_names)}
    global IDX_TO_NAME
    IDX_TO_NAME = {v: k for k, v in name_to_idx.items()}
    valve_names = [name_to_idx[name] for name in valve_names]
    tunnels_to = [[name_to_idx[name] for name in exits] for exits in tunnels_to]
    flow_rates = np.asarray(flow_rates, dtype=int)
    compute_distance_matrix(valve_names, tunnels_to)
    print(flow_rates)
    states: List[State] = [State([name_to_idx['AA'], name_to_idx['AA']], [False] * len(valve_names), 0, START_TIME, [])]

    best_released_pressure = 0
    idx = 0
    while (len(states) > 0):
        states = sorted(states, key=lambda s: (s.pressure_per_time(), s.time_left))
        current_state = states.pop()
        if current_state.released_pressure > best_released_pressure:
            best_released_pressure = current_state.released_pressure
            print(best_released_pressure)
        if current_state.time_left == 0:
            print(current_state)
            print("\n".join(current_state.story))
            print(current_state.released_pressure)
            break

        # Figure out the moves
        possible_new_states: List[List[Tuple[List[int, int], List[bool]]]] = [[], []]
        for agent_idx in range(2):
            if current_state.valve_in_current_room_can_be_opened(agent_idx, flow_rates):  # Open a valve
                new_opened_valves = deepcopy(current_state.opened_valves)
                new_opened_valves[current_state.locations[agent_idx]] = True
                possible_new_states[agent_idx].append((current_state.locations, new_opened_valves))

            for new_location in tunnels_to[current_state.locations[agent_idx]]:  # Move
                new_tuple_location = deepcopy(current_state.locations)
                new_tuple_location[agent_idx] = new_location
                possible_new_states[agent_idx].append((new_tuple_location, current_state.opened_valves))
        # Combine my and elephant new states
        combined_possible_new_states: List[Tuple[List[int, int], List[bool]]] = []
        for my_new_location, my_new_opened_valves in possible_new_states[0]:
            for elephant_new_location, elephant_new_opened_valves in possible_new_states[1]:
                combined_possible_new_states.append(([my_new_location[0], elephant_new_location[1]], [a or b for a, b in zip(my_new_opened_valves, elephant_new_opened_valves)]))
        # Create new states
        new_pressure = current_state.released_pressure + current_state.pressure_per_minute(flow_rates)
        new_time_left = current_state.time_left - 1
        for new_locations, new_opened_valves in combined_possible_new_states:
            new_state = State(
                locations=new_locations,
                opened_valves=new_opened_valves,
                released_pressure=new_pressure,
                time_left=new_time_left,
                story=[]
            )
            if is_better_than_existing_states(new_state, states):
                states.append(new_state)
        idx += 1


if __name__ == '__main__':
    main()





    # story = current_state.story + [
    #     f"== Minute {START_TIME - current_state.time_left + 1}==\n"
    #     f"Valves {list_open_valves(current_state)} are open, releasing {current_state.pressure_per_minute(flow_rates)}\n"
    #     f"You open valve {IDX_TO_NAME[current_state.location]}"
    # ]

# story = current_state.story + [
#     f"== Minute {START_TIME - current_state.time_left + 1}==\n"
#     f"Valves {list_open_valves(current_state)} are open, releasing {current_state.pressure_per_minute(flow_rates)}\n"
#     f"You move to valve {IDX_TO_NAME[new_location]}"
# ]
