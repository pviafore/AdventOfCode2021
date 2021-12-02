
def read_numbers(filename: str) -> list[int]:
    with open(filename) as f:
        return [int(stripped) for l in f if (stripped:=l.strip())]


def read_multiline(filename: str, func=lambda s:s) -> list:
    with open(filename) as f:
        return [func(l.strip()) for l in f if l.strip()]
