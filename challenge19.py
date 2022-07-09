import itertools
import re

from dataclasses import dataclass
from functools import lru_cache

def get_rotations() -> list[tuple[int,int,int]]:
    rotations = []
    for orientation in ORIENTATIONS:
        rotation = orientation
        rotations.append(rotation)
        for _ in range(3):
            a,b,c = rotation
            rotation = a,c,b*-1
            rotations.append(rotation)
    return rotations

ORIENTATIONS = [
    (1,2,3),
    (2,-1,3),
    (-1,-2,3),
    (-2,1,3),
    (-3,-1,2),
    (3,-2,1)
]
ROTATIONS = get_rotations()
Point = tuple[int, int, int]

def subtract_points(p1: Point, p2: Point) -> Point:
    return (p1[0] - p2[0], p1[1] - p2[1], p1[2] - p2[2])

def add_points(p1: Point, p2: Point) -> Point:
    return (p1[0] + p2[0], p1[1] + p2[1], p1[2] + p2[2])

def to_point(text: str) -> Point:
    parts = text.split(',')
    return int(parts[0]), int(parts[1]), int(parts[2])

@dataclass(frozen=True)
class ScannerReading:
    scanner: int
    beacons: tuple[Point, ...]

    def orient(self, rotation: tuple[int, int, int]) -> 'ScannerReading':
        new_beacons = []
        for beacon in self.beacons:
            value = [0,0,0]
            for index in range(3):
                value[index] = beacon[abs(rotation[index]) - 1]
                if rotation[index] < 0:
                    value[index] *= -1
            new_beacons.append(tuple(value))
        return ScannerReading(self.scanner, tuple(new_beacons)) # type: ignore

@dataclass
class Scanner:
    position: Point
    beacons_in_range: set[Point]

    def get_adjacent_scanner_options(self,
                                     orientation: ScannerReading
                                     ) -> list['Scanner']:
        adjacent: list[Scanner] = []
        num_beacons = len(orientation.beacons)
        for beacon, fixed_beacon in itertools.product(orientation.beacons,
                                                      self.beacons_in_range):
            scanner_position = subtract_points(fixed_beacon,
                                               beacon)  # type: ignore
            if all(a.position != scanner_position for a in adjacent):
                found = 0
                valid = True
                not_found = 0
                adjusted_beacons = set()
                for original_beacon in orientation.beacons:
                    adjusted_beacon = add_points(scanner_position,
                                                 original_beacon)
                    if self.in_range(adjusted_beacon):
                        if adjusted_beacon in self.beacons_in_range:
                            found += 1
                        else:
                            # in range, but not listed
                            valid = False
                            break
                    else:
                        not_found += 1
                        if not_found > num_beacons - 12:
                            valid = False
                            break
                    adjusted_beacons.add(adjusted_beacon)
                if found >= 12 and valid:
                    adjacent.append(Scanner(scanner_position,
                                            adjusted_beacons))
        return adjacent

    def in_range(self, point: Point) -> bool:
        return (abs(self.position[0] - point[0]) <= 1000 and
                abs(self.position[1] - point[1]) <= 1000 and
                abs(self.position[2] - point[2]) <= 1000)


def rotate(value1: int, value2: int, rotations: int ) -> tuple[int, int]:
    for _ in range(rotations):
        value1, value2 = value2, value1 * -1
    return value1, value2

def to_scanner_reading(lines: list[str]) -> ScannerReading:
    _,scanner_number,_ = re.split(r"(?:--- scanner )|(?: ---)", lines[0])
    points = [to_point(t.strip()) for t in lines[1:] if t]
    return ScannerReading(int(scanner_number), tuple(points))

@lru_cache
def orientations(scanner_reading: ScannerReading) -> list[ScannerReading]:
    # this is the list of the axis and negative means invert
    return [scanner_reading.orient(rotation) for rotation in ROTATIONS]


def find_solved_scanners(readings: list[ScannerReading]) -> list[Scanner]:
    origin = at_origin(readings[0])
    return deduce([origin], readings[1:], len(readings))

def find_number_of_beacons(scanners: list[Scanner]) -> int:
    return len(set(itertools.chain.from_iterable(s.beacons_in_range
                                                 for s in scanners)))

def get_distance_of_furthest_apart_scanners(scanners: list[Scanner]) -> int:
    scanner_pairs = itertools.product(scanners, scanners)
    return max(get_distance(s1, s2) for s1, s2 in scanner_pairs)

def get_distance(scanner1: Scanner, scanner2: Scanner):
    distance = subtract_points(scanner1.position, scanner2.position)
    return abs(distance[0]) + abs(distance[1]) + abs(distance[2])

def deduce(scanners: list[Scanner],
           scanner_readings: list[ScannerReading],
           expected_size: int) -> list[Scanner]:
    if not scanner_readings:
        return scanners
    for scanner_reading in scanner_readings:
        for orientation in orientations(scanner_reading):
            for scanner in scanners:
                matching_scanners = (
                    scanner.get_adjacent_scanner_options(orientation))
                for matching_scanner in matching_scanners:
                    new_readings = [sr for sr in scanner_readings
                                    if sr != scanner_reading]
                    new_scanners = scanners + [matching_scanner]
                    answer = deduce(new_scanners, new_readings, expected_size)
                    if answer and len(answer) == expected_size:
                        return answer
    return [] # not a viable answer


def at_origin(scanner_reading: ScannerReading) -> Scanner:
    # assumes the first one is at origin
    return Scanner((0,0,0), set(scanner_reading.beacons))


with open("input/input19.txt", encoding="utf-8") as f:
    SCANNER_READINGS = [to_scanner_reading(sr.split('\n'))
                        for sr in f.read().split('\n\n')]

if __name__ == "__main__":
    solved_scanners = find_solved_scanners(SCANNER_READINGS)
    print(f"Number of beacons: {find_number_of_beacons(solved_scanners)}")
    print(f"Distance on furthest scanners: "
          f"{get_distance_of_furthest_apart_scanners(solved_scanners)}")
