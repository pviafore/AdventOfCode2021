
from collections import Counter
from typing import Optional

from common.file_input import read_multiline
from common.grid import Grid, Point


def get_total_risk_level(grid: Grid) -> int:
    low_values = [value for point, value in grid.items()
                  if all(value < n for _,n in grid.get_neighbors(point, 10))]
    return sum(low_values) + len(low_values)


def get_largest_basins_product(grid: Grid) -> int:
    basins = get_basin_sizes(grid)
    sorted_basins = sorted(basins, reverse=True)
    return sorted_basins[0] * sorted_basins[1] * sorted_basins[2]


def get_basin_sizes(grid: Grid) -> list[int]:
    basin_id = 0
    basin_assignment: dict[Point, Optional[int]] = {}
    for point, value in grid.items():
        if value != 9:
            x, y = point
            above = basin_assignment.get((x, y - 1), None)
            left = basin_assignment.get((x - 1, y), None)
            if above is not None and left is not None:
                basin_assignment[point] = left
                # merge basins
                for basin_point, assignment in basin_assignment.items():
                    if assignment == above:
                        basin_assignment[basin_point] = left
            elif above is None and left is None:
                # new basin
                basin_assignment[point] = basin_id
                basin_id += 1
            elif above is not None:
                basin_assignment[point] = above
            elif left is not None:
                basin_assignment[point] = left
        else:
            basin_assignment[point] = None
    counter: Counter[int] = Counter([v for v in basin_assignment.values()
                                     if v is not None])
    return list(counter.values())


GRID: Grid[str] = Grid(read_multiline("input/input9.txt"), func=int)

if __name__ == "__main__":
    print(f"Total Risk Level: {get_total_risk_level(GRID)}")
    print(f"# largest basins sum {get_largest_basins_product(GRID)}")
