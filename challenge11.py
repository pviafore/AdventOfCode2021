import itertools
from copy import deepcopy
from typing import Optional

from common.file_input import read_multiline
from common.grid import Grid

Octopus = Optional[int]

def get_number_of_flashes(octopodes: Grid[Octopus]) -> int:
    return sum(flash(octopodes) for _ in range(100))

def get_synchronization(octopodes: Grid[Octopus]) -> int:
    for num in itertools.count(start=1):
        flash(octopodes)
        # they all just flashed
        if all(o == 0 for o in octopodes.values()):
            return num

    raise RuntimeError("Should never get here")

def flash(octopodes: Grid[Octopus]) -> int:
    flashes = 0

    for point in octopodes:
        octopodes[point] += 1

    potentials = [point for point, octopus in octopodes.items()
                  if octopus == 10]
    while potentials:
        point = potentials.pop(0)
        for neighbor_point,neighbor in octopodes.get_neighbors(point, None,
                                                               diagonal=True):
            if neighbor and neighbor != 10:
                #update original grid point
                octopodes[neighbor_point] += 1
                # it's getting bumped to >9
                if neighbor == 9:
                    potentials.append(neighbor_point)
    # reset and count flashes
    for point, octopus in octopodes.items():
        if octopus == 10:
            flashes += 1
            octopodes[point] = 0
    return flashes

OCTOPODES: Grid[Octopus] = Grid(read_multiline("input/input11.txt"), int)

if __name__ == "__main__":
    print(f"# of flashes: {get_number_of_flashes(deepcopy(OCTOPODES))}")
    print(f"Synchronization: {get_synchronization(deepcopy(OCTOPODES))}")
