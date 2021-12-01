from dataclasses import dataclass
from typing import Optional

from common.file_input import read_multiline


DIGIT_SEGMENTS = ("abcefg", "cf", "acdeg", "acdfg", "bcdf", "abdfg",
                  "abdefg", "acf", "abcdefg", "abcdfg")


@dataclass
class DigitDisplay:
    inputs: list[str]
    outputs: list[str]


def to_digital_display(text: str) -> DigitDisplay:
    inputs, outputs = text.split(' | ')
    return DigitDisplay(inputs.split(" "), outputs.split(" "))


def get_number_of_easy_numbers(digit_displays: list[DigitDisplay]) -> int:
    return sum(len(get_easy_numbers(d.outputs)) for d in digit_displays)


def get_easy_numbers(outputs: list[str]):
    return [n for n in outputs if len(n) in (2, 3, 4, 7)]


def get_decoded_sum(digit_displays: list[DigitDisplay]) -> int:
    return sum(decode(d) for d in digit_displays)


def decode(digit_display: DigitDisplay) -> int:
    translation_table = build_translation_table(digit_display.inputs)
    outputs = [code.translate(translation_table)
               for code in digit_display.outputs]
    return int(''.join([str(DIGIT_SEGMENTS.index(''.join(sorted(o))))
                        for o in outputs]))


def build_translation_table(inputs: list[str]) -> dict[int, int]:
    translation_table = deduce_solution(inputs, {})
    assert translation_table is not None
    return {ord(k): ord(v) for k, v in translation_table.items()}


def deduce_solution(inputs: list[str],
                    mapping: dict[str, str]) -> Optional[dict[str, str]]:
    remaining_letters = [k for k in "abcdefg" if k not in mapping.keys()]
    remaining_values = [v for v in "abcdefg" if v not in mapping.values()]
    if not remaining_letters:
        return mapping
    next_letter = remaining_letters.pop()
    for value in remaining_values:
        potential_lengths = [len(d) for d in DIGIT_SEGMENTS if value in d]
        matching_lengths = [len(i) for i in inputs if next_letter in i]
        if sorted(potential_lengths) == sorted(matching_lengths):
            new_mapping = mapping | {next_letter: value}
            if (potential := deduce_solution(inputs, new_mapping)) is not None:
                return potential
    return None


DIGIT_DISPLAYS = read_multiline("input/input8.txt", to_digital_display)
if __name__ == "__main__":
    print(f"# of Easy Numbers: {get_number_of_easy_numbers(DIGIT_DISPLAYS)}")
    print(f"Decoded sum = {get_decoded_sum(DIGIT_DISPLAYS)}")
