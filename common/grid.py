
import functools
import itertools

from collections import UserDict
from typing import Callable, Generator, Generic, TypeVar

Point = tuple[int, int]

T = TypeVar('T')

@functools.lru_cache
def get_neighboring_points(point: Point, diagonal=False):
    x,y = point
    points = [(x, y-1),(x-1, y), (x+1, y), (x, y+1)]
    if diagonal:
        points += [(x-1, y-1), (x-1, y+1), (x+1, y-1), (x+1, y+1)]
    return points


class Grid(UserDict, Generic[T]):

    def __init__(self, lines: list[str], func: Callable = lambda s: s):
        super().__init__()
        self.data: dict[Point, T] ={(x,y): func(lines[y][x])
                                    for x,y in _get_grid_points(lines)}

    # returns the neighbors a up, left, right, down
    def get_neighbors(self, point: Point, default_value: T,
                      diagonal=False) -> list[tuple[Point, T]]:
        neighbor_points = get_neighboring_points(point, diagonal)
        return [(p, self.data.get(p, default_value)) for p in neighbor_points]

    def get_max_x(self, row_index: int) -> int:
        return max(p[0] for p in self.data.keys() if p[1] == row_index)

    def get_max_y(self, col_index: int) -> int:
        return max(p[1] for p in self.data.keys() if p[0] == col_index)

    # get points outside the gride
    def get_outskirt_points(self) -> list[Point]:
        xes = {x for x,_ in self.data.keys()}
        yes = {y for _,y in self.data.keys()}
        min_x = min(xes)
        max_x = max(xes)
        min_y = min(yes)
        max_y = max(yes)
        borders = (list(itertools.product([min_x - 1, max_x + 1], yes)) + # type: ignore
                   list(itertools.product(xes, [min_y - 1, max_y + 1])))
        corners = list(itertools.product([min_x - 1, max_x + 1],
                                         [min_y - 1, max_y + 1]))
        return borders + corners

    def __str__(self) -> str:
        xes = [x for x, _ in self.data.keys()]
        yes = [y for _, y in self.data.keys()]
        min_x = min(xes)
        max_x = max(xes)
        min_y = min(yes)
        max_y = max(yes)
        outstr: str = ''
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                outstr += str(self.data.get((x, y), ' ')) # type: ignore
            outstr += '\n'
        return outstr


def _get_grid_points(grid: list[str]) -> Generator[Point, None, None]:
    for row_index, row in enumerate(grid):
        for column_index, _ in enumerate(row):
            yield column_index,row_index
