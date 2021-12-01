import copy
import itertools

from common.file_input import read_multiline
from common.grid import Grid, Point

def get_right_point(point: Point, max_x) -> Point:
    return ((point[0] + 1) % (max_x + 1), point[1])

def get_lower_point(point: Point, max_y) -> Point:
    return (point[0], (point[1] + 1) % (max_y + 1))

def get_turns_until_stasis(cucumbers: Grid[str]) -> int:
    points = {p: s for p, s in cucumbers.items() if s != '.'}

    max_x = cucumbers.get_max_x(0)
    max_y = cucumbers.get_max_y(0)

    for turn in itertools.count(1):
        moved = False
        old_state = copy.deepcopy(points)
        for point, symbol in old_state.items():
            next_point = get_right_point(point, max_x)
            if symbol == '>' and next_point not in old_state:
                del points[point]
                points[next_point] = '>'
                moved = True

        older_state = copy.deepcopy(points)
        for point, symbol in old_state.items():
            next_point = get_lower_point(point, max_y)
            if symbol == 'v' and next_point not in older_state:
                del points[point]
                points[next_point] = 'v'
                moved = True

        if not moved:
            return turn

    assert False, "Can not reach here"

CUCUMBERS = Grid(read_multiline("input/input25.txt"))

if __name__ == "__main__":
    print(f"Turns until stasis: {get_turns_until_stasis(CUCUMBERS)}")
