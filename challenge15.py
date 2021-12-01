import heapq

from math import sqrt

from common.file_input import read_multiline
from common.grid import Grid, Point

def get_lowest_risk(grid: Grid[int]):
    grid_side_length = int(sqrt(len(grid)))
    start = (0, 0)
    end = (grid_side_length-1, grid_side_length-1)
    smallest_cost = 10*len(grid)*len(grid)
    heap_queue: list[tuple[int, Point, set[Point]]] = [(0, start, set())]
    while heap_queue:
        cost, point, seen = heapq.heappop(heap_queue)
        if point in seen:
            continue
        if cost > smallest_cost:
            continue
        if point == end:
            smallest_cost = cost
            continue
        seen.add(point)
        neighbors = grid.get_neighbors(point, -1) # type: ignore
        for neighbor, value in neighbors:
            if value != -1:
                heapq.heappush(heap_queue, (cost + value, # type:ignore
                                            neighbor, seen))
    return smallest_cost

def get_lowest_risk_big_grid(grid: Grid[int]) -> int:
    grid_side_length = int(sqrt(len(grid)))
    new_grid: Grid[int] = Grid([], int)
    for i in range(5):
        for j in range(5):
            for point, value in grid.items():
                x,y = point
                new_point = (i*grid_side_length + x, j*grid_side_length + y)
                new_value = value + i + j
                while new_value >= 10:
                    new_value = new_value - 10 + 1
                new_grid[new_point] = new_value
    return get_lowest_risk(new_grid)


GRID: Grid[int] = Grid(read_multiline('input/input15.txt'), int)

if __name__ == "__main__":
    print(f"Lowest Risk Value: {get_lowest_risk(GRID)}")
    print(f"Lowest Risk Value (big grid): {get_lowest_risk_big_grid(GRID)}")
