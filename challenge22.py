import re
import itertools

from dataclasses import dataclass
from typing import Iterator

from common.file_input import read_multiline


Point = tuple[int, int, int]


@dataclass(frozen=True)
class Cuboid:
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    z_min: int
    z_max: int

    def __bool__(self) -> bool:
        return (self.x_min <= self.x_max and self.y_min <= self.y_max
                and self.z_min <= self.z_max)

    def contains(self, rhs: 'Cuboid') -> bool:
        return (self.x_min <= rhs.x_min and self.x_max >= rhs.x_max and
                self.y_min <= rhs.y_min and self.y_max >= rhs.y_max and
                self.z_min <= rhs.z_min and self.z_max >= rhs.z_max)

    def __iter__(self) -> Iterator:
        return itertools.product(range(self.x_min, self.x_max + 1),
                                 range(self.y_min, self.y_max + 1),
                                 range(self.z_min, self.z_max + 1))

    def intersects(self, rhs: 'Cuboid') -> bool:
        return (self.x_min <= rhs.x_max and self.x_max >= rhs.x_min and
                self.y_min <= rhs.y_max and self.y_max >= rhs.y_min and
                self.z_min <= rhs.z_max and self.z_max >= rhs.z_min)

    def get_area(self):
        return ((1 + self.x_max - self.x_min) * (1 + self.y_max - self.y_min) *
                (1 + self.z_max - self.z_min))

    def get_external_cubes(self, cube: 'Cuboid',) -> list['Cuboid']:

        # Assuming our dimensions are Sx, Sy, Sz
        # and our sides are (SXmin, SXmax), (SYmin, SYmax), (SZmin, SZmax)
        # Given the cuboid with dimensions Cx, Cy, Cz and the
        # and its sides are (CXmin, CXmax), (CYmin, CYmax), (CZmin, CZmax)
        # with an intercept area of
        # Xmin, Xmax, Ymin, Ymax, Zmin, zmax

        # if it intersects the cube, there are 6 cuboids that need to
        # be prepended to the list to check
        # with the following dimensions
        # C1 = (Xmin, Xmax), (CYmax, Ymax),  (Zmin, Zmax)
        #    located above the intersection with same x,z
        # C2 = (Xmin, Xmax), (Ymin, CYmin),  (Zmin, Zmax)
        #    located benath the intersection with same x,z
        # C3 = (CXmin, Xmin), (CYmin, CYmax), (Zmin, Zmax)
        #    located to the left of intersection, with full height,
        #    same z
        # C4 = (Xmax, CXmax), (CYmin, CYmax), (Zmin, Zmax)
        #    located to the right of intersection, with full height,
        #    same z
        # C5 = (CXmin, CXmax), (CYmin, CYmax), (Zmin, CZmin)
        #    located in front of intersection, full height/width
        # C6 = (CXmin, CXmax), (CYmin, CYmax), (CZmax, Zmax)
        #    located in front of intersection, full height/width

        # intercept dimensions
        if self.x_min <= cube.x_min <= cube.x_max <= self.x_max:
            xrange = (cube.x_min, cube.x_max)
        elif cube.x_min <= self.x_min <= self.x_max <= cube.x_max:
            xrange = (self.x_min, self.x_max)
        elif self.x_min <= cube.x_min < self.x_max < cube.x_max:
            xrange = (cube.x_min, self.x_max)
        elif cube.x_min < self.x_min <= cube.x_max <= self.x_max:
            xrange = (self.x_min, cube.x_max)
        else:
            assert False, "Missing condition"

        if self.z_min <= cube.z_min <= cube.z_max <= self.z_max:
            zrange = (cube.z_min, cube.z_max)
        elif cube.z_min <= self.z_min <= self.z_max <= cube.z_max:
            zrange = (self.z_min, self.z_max)
        elif self.z_min <= cube.z_min < self.z_max < cube.z_max:
            zrange = (cube.z_min, self.z_max)
        elif cube.z_min < self.z_min <= cube.z_max <= self.z_max:
            zrange = (self.z_min, cube.z_max)
        else:
            assert False, "Missing z condition"

        new_cubes = [
            Cuboid(*xrange, self.y_max + 1, cube.y_max, *zrange),
            Cuboid(*xrange, cube.y_min, self.y_min - 1, *zrange),
            Cuboid(cube.x_min, self.x_min - 1, cube.y_min, cube.y_max,
                   *zrange),
            Cuboid(self.x_max + 1, cube.x_max, cube.y_min, cube.y_max,
                   *zrange),
            Cuboid(cube.x_min, cube.x_max, cube.y_min, cube.y_max,
                   cube.z_min, self.z_min - 1),
            Cuboid(cube.x_min, cube.x_max, cube.y_min, cube.y_max,
                   self.z_max + 1, cube.z_max)
        ]
        valid_cubes = [c for c in new_cubes if c]
        assert(sum(c.get_area() for c in new_cubes if c) < cube.get_area())
        return valid_cubes


@dataclass
class CuboidInstruction:
    on: bool
    cuboid: Cuboid


def to_cuboid_instruction(text: str) -> CuboidInstruction:
    split = re.split(r' x=|\.\.|,y=|,z=', text)
    x_min, x_max = sorted([int(split[1]), int(split[2])])
    y_min, y_max = sorted([int(split[3]), int(split[4])])
    z_min, z_max = sorted([int(split[5]), int(split[6])])
    return CuboidInstruction(split[0] == "on", Cuboid(x_min, x_max, y_min,
                                                      y_max, z_min, z_max))


INSTRUCTIONS: list[CuboidInstruction] = read_multiline("input/input22.txt",
                                                       to_cuboid_instruction)
INITIALIZATION_AREA = Cuboid(-50, 50, -50, 50, -50, 50)


def get_cubes_on_in_initialization_area(
        instructions: list[CuboidInstruction]) -> int:

    cubes: dict[tuple[int, int, int], bool] = {}
    for instruction in instructions:
        if INITIALIZATION_AREA.contains(instruction.cuboid):
            for x, y, z in instruction.cuboid:
                cubes[(x, y, z)] = instruction.on

    return len([v for v in cubes.values() if v])


def get_all_cubes_on(instructions: list[CuboidInstruction]) -> int:
    # reverse the instructions because they will be the last applied
    instructions_to_apply = list(reversed(instructions))
    finalized_cubes: dict[Cuboid, bool] = {}
    while instructions_to_apply:
        instruction = instructions_to_apply.pop(0)
        cuboid = instruction.cuboid
        # we need to take a look at the current cube
        is_candidate = True
        for cube in finalized_cubes:
            # if its inside any other cube completely, ignore it
            if cube.contains(cuboid):
                is_candidate = False
                break

            # if its completely outside any other cube, add it to the list
            # otherwise, it intersects the cube
            if cube.intersects(cuboid):

                new_cubes = cube.get_external_cubes(cuboid)
                new_instructions = [CuboidInstruction(instruction.on, c)
                                    for c in new_cubes]
                instructions_to_apply = (new_instructions +
                                         instructions_to_apply)

                is_candidate = False
                break

        if is_candidate:
            for cube in finalized_cubes:
                assert not cube.intersects(instruction.cuboid)

            assert instruction.cuboid not in finalized_cubes
            finalized_cubes[instruction.cuboid] = instruction.on

    return sum(cube.get_area()
               for cube, is_on in finalized_cubes.items()
               if is_on)


if __name__ == "__main__":
    cubes_on = get_cubes_on_in_initialization_area(INSTRUCTIONS)
    print(f"Cubes On In Initialization Procedure Area: {cubes_on}")
    all_cubes_on = get_all_cubes_on(INSTRUCTIONS)
    print(f"All Cubes On: {all_cubes_on}")
