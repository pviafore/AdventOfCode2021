import functools

from dataclasses import dataclass

from common.file_input import read_multiline

@dataclass
class Instruction:
    op: str
    variable: str
    operand: str | int | None


def to_instruction(text: str) -> Instruction:
    split = text.split(" ")
    try:
        operand: int | str | None = int(split[2])
    except ValueError:
        operand = split[2]
    except IndexError:
        operand = None

    assert split[0] in ["inp", "add", "mul", "div", "mod", "eql"]
    return Instruction(split[0], split[1], operand)

#  gathered from computer program
z_divides = [1, 1, 1, 1, 26, 26, 26, 1, 1, 26, 26, 26, 1, 26]
initial_xes = [13, 15, 15, 11, -16, -11, -6, 11, 10, -10, -8, -11, 12, -15]
y_adds = [5, 14, 15, 16, 8, 9, 2, 13, 16, 6, 6, 9, 11, 5]

assert len(z_divides) == len(initial_xes) == len(y_adds) == 14


# z = z// Zi
# if z%26 + Xi == Di:
#    z = z*26 + Di + Yi


def reduction(counter: int, z: int) -> list[int]:
    if counter == -1:
        return [0]
    possible_digits: list[str] = []
    for possible_digit in range(9, 0, -1):
        # checking if z%26 + Xi can == Di
        target_z = range(z * z_divides[counter],
                         (z + 1) * z_divides[counter])
        for previous_z in target_z:
            if previous_z % 26 + initial_xes[counter] == possible_digit:
                possible_digits.extend([
                    possible_digit * int(pow(10, len(y_adds) - counter - 1)) + s
                    for s in reduction(counter - 1, previous_z)
                ])

        candidate = (z - possible_digit - y_adds[counter]) // 26
        target_z = range(candidate * z_divides[counter],
                         (candidate + 1) * z_divides[counter])
        for previous_z in target_z:
            # make sure that we are in the else clause, and that
            # the digit is possible
            if ((z == (previous_z // z_divides[counter] * 26
                       + possible_digit + y_adds[counter])) and
                    previous_z % 26 + initial_xes[counter] != possible_digit):
                possible_digits.extend([
                    possible_digit * int(pow(10, len(y_adds) - counter - 1)) + s
                    for s in reduction(counter - 1, previous_z)
                ])
    return possible_digits


INSTRUCTIONS: list[Instruction] = read_multiline("input/input24.txt",
                                                 to_instruction)

if __name__ == "__main__":
    values = reduction(len(initial_xes) - 1, 0)
    print(f"Max valid number = {max(values)}")
    print(f"Min valid number = {min(values)}")
