import itertools
import re

from functools import lru_cache
from typing import Generator

Target = tuple[int, int, int, int]
def to_target(text: str) -> Target:
    parts = re.split(r'(?:target area: x=)|(?:\.\.)|(?:, y=)', text)
    return (int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]))

# only good for positive y-velocities
def get_highest_y(target:  Target) -> int:
    upper_bound = abs(target[2])
    return upper_bound * (upper_bound -1) // 2

def get_total_number_of_shots(target: Target) -> int:
    points = itertools.product(range(get_first_x_value(target), target[1]+1),
                               range(target[2], -1*target[2] + 1))

    new_values = set()
    for x,y in points:
        total_x = 0
        total_y = 0
        x_step = x
        y_step = y
        while total_x <= target[1] and total_y >= target[2]:
            total_x += x_step
            total_y += y_step
            if x_step > 0:
                x_step -=1
            y_step -= 1
            if target[0] <= total_x <= target[1] and target[2] <= total_y <= target[3]:
                new_values.add((x,y))

    return len(new_values)


def accumulator() -> Generator[tuple[int, int], None, None]:
    yield from zip(itertools.count(start=1), itertools.accumulate(itertools.count(start=1)))


def get_first_x_value(target: Target) -> int:
    return next(i for i,sum in accumulator() if sum >= target[0])


with open("input/input17.txt", encoding="utf-8") as f:
    TARGET = to_target(f.read().strip())

if __name__ == "__main__":
    print(f"Highest y: {get_highest_y(TARGET)}")
    print(f"Possible Values: {get_total_number_of_shots(TARGET)}")
