
def read_numbers(filename: str) -> list[int]:
    with open(filename) as f:
        return [int(stripped) for l in f if (stripped:=l.strip())]
