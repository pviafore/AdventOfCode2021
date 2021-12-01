import itertools

from collections import Counter
from dataclasses import dataclass

from common.file_input import read_multiline


@dataclass(frozen=True)
class Point:
    x_pos: int
    y_pos: int


@dataclass
class LineSegment:
    start: Point
    end: Point

    def get_all_points(self) -> list[Point]:
        slope_modifier = self._get_slope_modifier()
        points = [self.start]
        while (last_point := points[-1]) != self.end:
            points.append(Point(last_point.x_pos + slope_modifier[0],
                                last_point.y_pos + slope_modifier[1]))
        return points

    # x,y
    def _get_slope_modifier(self) -> tuple[int, int]:
        x_modifier = -1 if self.start.x_pos > self.end.x_pos else 1
        y_modifier = -1 if self.start.y_pos > self.end.y_pos else 1
        if self.is_vertical():
            return (0, y_modifier)
        if self.start.y_pos == self.end.y_pos:
            return (x_modifier, 0)
        return (x_modifier, y_modifier)

    def is_vertical(self):
        return self.start.x_pos == self.end.x_pos

    def get_slope(self) -> float:
        slope_modifier = self._get_slope_modifier()
        assert slope_modifier[0] != 0
        return slope_modifier[1] / slope_modifier[0]


def to_line(text: str) -> LineSegment:
    points = text.split(' -> ')
    return LineSegment(to_point(points[0]), to_point(points[1]))


def to_point(text: str) -> Point:
    pieces = text.split(',')
    return Point(int(pieces[0]), int(pieces[1]))


def get_number_of_overlapping_points_no_diagonal(
            lines: list[LineSegment]) -> int:

    non_diagonal = [l for l in lines if l.is_vertical() or l.get_slope() == 0]
    return get_number_of_overlapping_points(non_diagonal)


def get_number_of_overlapping_points(lines: list[LineSegment]) -> int:
    all_points = itertools.chain.from_iterable(
        line.get_all_points() for line in lines)
    overlaps = Counter(all_points)
    return len([val for val, count in overlaps.items() if count >= 2])


LINES = read_multiline("input/input5.txt", to_line)

if __name__ == "__main__":
    print(f"# of overlaps: "
          f"{get_number_of_overlapping_points_no_diagonal(LINES)}")
    print(f"# of overlaps (w/ diagonal): "
          f"{get_number_of_overlapping_points(LINES)}")
