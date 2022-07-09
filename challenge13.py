import re

from dataclasses import dataclass
from enum import Enum

class Direction(Enum):
    HORIZONTAL = "H"
    VERTICAL = "Y"

Point = tuple[int, int]
Fold = tuple[Direction, int]

@dataclass
class Instructions:
    points: list[Point]
    folds: list[Fold]

def to_instructions(text: list[str]):
    split_point = text.index('\n')
    points = [to_point(p.strip()) for p in text[:split_point]]
    folds = [to_fold(f.strip()) for f in text[split_point + 1:]]
    return Instructions(points, folds)

def to_point(point: str) -> Point:
    x,y = point.split(",")
    return (int(x), int(y))

def to_fold(fold: str) -> Fold:
    *_,axis,value = re.split('[ =]', fold)
    return (Direction.HORIZONTAL if axis == 'x' else Direction.VERTICAL,
            int(value))

def get_visible_points_after_first_fold(instructions: Instructions) -> int:
    points = make_fold(instructions.points, instructions.folds[0])
    return len(points)

def make_fold(points: list[Point], fold: Fold) -> list[Point]:
    if fold[0] == Direction.VERTICAL:
        normal_half = [p for p in points if p[1] < fold[1]]
        to_be_reversed = [p for p in points if p[1] > fold[1]]
        reverse = [(x, 2*fold[1]-y)
                    for x,y in to_be_reversed]
    else:
        normal_half = [p for p in points if p[0] < fold[1]]
        to_be_reversed = [p for p in points if p[0] > fold[1]]
        reverse = [(2*fold[1]-x, y)
                    for x,y in to_be_reversed]
    return list(set([*normal_half, *reverse]))

def show_code(instructions: Instructions):
    points = instructions.points
    for instruction in instructions.folds:
        points = make_fold(points, instruction)
    assert points, "Points should be non zero length"
    unique_points = set(points)
    xes = [x for x, _ in points]
    yes = [y for _, y in points]
    for row in range(min(yes), max(yes)+1):
        for column in range(min(xes), max(xes)+1):
            letter = '*' if (column, row) in unique_points else ' '
            print(letter, end="")
        print()

with open("input/input13.txt", encoding="utf-8") as f:
    INSTRUCTIONS = to_instructions(f.readlines())

if __name__ == "__main__":
    print(f"Points visible after first fold: "
          f"{get_visible_points_after_first_fold(INSTRUCTIONS)}")
    show_code(INSTRUCTIONS)
