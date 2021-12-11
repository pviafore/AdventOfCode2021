
from collections import Counter
from typing import Generator, Optional

from common.file_input import read_multiline

def get_neighbors(grid: list[str], x: int,
                  y: int) -> tuple[int, int, int, int]:
    top, left, right, bottom = (10, 10, 10, 10)
    if y > 0:
        top = int(grid[y-1][x])
    if y < len(grid) -1:
        bottom = int(grid[y+1][x])
    if x > 0:
        left = int(grid[y][x-1])
    if x < len(grid[y]) - 1:
        right = int(grid[y][x+1])
    return (top, left, bottom, right)


def get_total_risk_level(grid: list[str]) -> int:
    low_points = [(x,y) for x,y in get_grid_points(grid)
                if all(int(grid[y][x]) < n for n in get_neighbors(grid, x, y))]
    return sum(1 + int(grid[y][x]) for x,y in low_points)

def get_grid_points(grid: list[str]) -> Generator[tuple[int, int], None, None]:
    for row_index,row in enumerate(grid):
        for column_index, _ in enumerate(row):
            yield column_index,row_index

def get_largest_basins_product(grid: list[str]) -> int:
    basins = get_basin_sizes(grid)
    sorted_basins = sorted(basins, reverse=True)
    return sorted_basins[0] * sorted_basins[1] * sorted_basins[2]

def get_basin_sizes(grid: list[str]) -> list[int]:
    basin_id = 0
    basin_assignment: dict[tuple[int, int], Optional[int]] = {}
    for x,y in get_grid_points(grid):
        if grid[y][x] != '9':
            above = basin_assignment.get((x, y - 1), None)
            left = basin_assignment.get((x - 1, y), None)
            if above is not None and left is not None:
                basin_assignment[(x,y)] = left
                # merge basins
                for point, assignment in basin_assignment.items():
                    if assignment == above:
                        basin_assignment[point] = left
            elif above is None and left is None:
                # new basin
                basin_assignment[(x,y)] = basin_id
                basin_id += 1
            elif above is not None:
                basin_assignment[(x,y)] = above
            elif left is not None:
                basin_assignment[(x,y)] = left
        else:
            basin_assignment[(x,y)] = None
    counter: Counter[int] = Counter([v for v in basin_assignment.values()
                                     if v is not None])
    return list(counter.values())


GRID = read_multiline("input/input9.txt")

if __name__ == "__main__":
    print(f"Total Risk Level: {get_total_risk_level(GRID)}")
    print(f"# largest basins sum {get_largest_basins_product(GRID)}")
