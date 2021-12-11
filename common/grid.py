from collections import UserDict
from typing import Callable, Generator, Generic, TypeVar

Point = tuple[int, int]

T = TypeVar('T')
class Grid(UserDict, Generic[T]):

    def __init__(self, lines: list[str], func: Callable=lambda s:s):
        super().__init__()
        self.data: dict[Point, T] ={(x,y): func(lines[y][x])
                                    for x,y in _get_grid_points(lines)}

    # returns the neighbors a up, left, right, down
    def get_neighbors(self, point: Point, default_value:T,
                      diagonal=False) -> list[tuple[Point, T]]:
        x,y = point
        points = [((x, y-1), self.data.get((x, y-1), default_value)),
                  ((x-1, y), self.data.get((x-1, y), default_value)),
                  ((x+1, y), self.data.get((x+1, y), default_value)),
                  ((x, y+1), self.data.get((x, y+1), default_value))]
        if diagonal:
            points += [((x-1, y-1), self.data.get((x-1, y-1), default_value)), # type: ignore
                       ((x-1, y+1), self.data.get((x-1, y+1), default_value)),
                       ((x+1, y-1), self.data.get((x+1, y-1), default_value)),
                       ((x+1, y+1), self.data.get((x+1, y+1), default_value))]
        return points


def _get_grid_points(grid: list[str]) -> Generator[Point, None, None]:
    for row_index,row in enumerate(grid):
        for column_index, _ in enumerate(row):
            yield column_index,row_index
