from typing import Callable

from common.file_input import read_multiline

LINES = read_multiline("input/input10.txt")

CLOSING_LETTER = {
    '[': ']',
    '{': '}',
    '<': '>',
    '(': ')'
}
def get_corrupted_score(lines: list[str]) -> int:
    return sum(get_corrupt_score(line) for line in lines)

def get_corrupt_score(line: str) -> int:
    score = 0

    def set_corrupt_score(letter: str):
        nonlocal score
        score = {
            ')': 3,
            ']': 57,
            '}': 1197,
            '>': 25137
        }[letter]

    parse(line, on_corrupt=set_corrupt_score)
    return score

def get_incomplete_score(lines: list[str]) -> int:
    scores = [score for line in lines
               if (score := get_incompleted_score(line))]
    return sorted(scores)[len(scores) // 2]

def get_incompleted_score(line: str) -> int:
    score = 0

    def set_incomplete_score(text: str):
        nonlocal score
        for letter in reversed(text):
            closing_letter = CLOSING_LETTER[letter]
            score *= 5
            score += {
                ')': 1,
                ']': 2,
                '}': 3,
                '>': 4
            }[closing_letter]

    parse(line, on_incomplete=set_incomplete_score)
    return score

def parse(line: str,
          on_corrupt: Callable[[str], None] = lambda _: None,
          on_incomplete: Callable[[str], None] = lambda _: None
         ):
    stack: list[str] = []
    for letter in line:
        if letter in "{[(<":
            stack.append(letter)
        if letter in ">]})":
            closing_letter = CLOSING_LETTER[stack.pop(-1)]
            if letter != closing_letter:
                on_corrupt(letter)
                return
    if stack:
        on_incomplete(''.join(stack))

if __name__ == "__main__":
    print(f"Corrupted Score: {get_corrupted_score(LINES)}")
    print(f"Incomplete Score: {get_incomplete_score(LINES)}")
