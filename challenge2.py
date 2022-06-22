from common.file_input import read_multiline

Move = tuple[str, int]
Position = tuple[int, int]
ImprovedPosition = tuple[int, int, int]


def get_position_value(moves: list[Move]) -> int:
    position = (0, 0)
    for move in moves:
        position = make_move(move, position)
    return position[0] * position[1]


def make_move(move: Move, position: Position) -> Position:
    if move[0] == 'forward':
        return (position[0] + move[1], position[1])
    if move[0] == 'down':
        return (position[0], position[1] + move[1])
    if move[0] == 'up':
        return (position[0], position[1] - move[1])
    raise RuntimeError('Invalid Move')


def get_improved_position_value(moves: list[Move]) -> int:
    position = (0, 0, 0)
    for move in moves:
        position = make_improved_move(move, position)
    return position[0] * position[1]


def make_improved_move(move: Move,
                       position: ImprovedPosition) -> ImprovedPosition:
    if move[0] == 'forward':
        return (position[0] + move[1], position[1] + (move[1] * position[2]),
                position[2])
    if move[0] == 'down':
        return (position[0], position[1], position[2] + move[1])
    if move[0] == 'up':
        return (position[0], position[1], position[2] - move[1])
    raise RuntimeError('Invalid Move')


def parse_move(text: str) -> Move:
    values = text.split(' ')
    assert values[0] in ['forward', 'down', 'up']
    return (values[0], int(values[1]))


MOVES: list[Move] = read_multiline("input/input2.txt", parse_move)


if __name__ == "__main__":
    print(f"Position value: {get_position_value(MOVES)}")
    print(f"Position value (improved): {get_improved_position_value(MOVES)}")
