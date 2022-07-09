from collections import UserList
from copy import deepcopy
from typing import Optional

# we'll use a bool to indicate marked
class Row(UserList): # type: ignore
    def __init__(self, values: list[int]):
        super().__init__()
        assert len(values) == 5
        self.data = values
        self.marked = [False for _ in values]

    def get_sum(self) -> int:
        return sum(v for v,marked in zip(self.data,self.marked)
                   if not marked)

    def is_all_marked(self) -> bool:
        return all(self.marked)

    def is_marked(self, index: int) -> bool:
        return self.marked[index]

    def mark(self, index: int):
        self.marked[index] = True


class Board:

    def __init__(self, rows: list[Row]):
        assert len(rows) == 5
        self.rows: list[Row] = rows

    def has_won(self) -> bool:
        return (any(row.is_all_marked() for row in self.rows) or
                any(self.is_column_marked(index)
                    for index in range(len(self.rows[0]))))

    def is_column_marked(self, index: int) -> bool:
        return all(row.is_marked(index) for row in self.rows)

    def get_score(self) -> int:
        return sum(row.get_sum() for row in self.rows)

    def apply_move(self, move: int):
        for row in self.rows:
            try:
                position = row.index(move)
                row.mark(position)
            except ValueError:
                pass

class Game:

    def __init__(self, moves: list[int], boards: list[Board]):
        self.moves = moves
        self.boards = boards
        self.last_move: int = 0

    def get_winning_board(self) -> Optional[Board]:
        return next((b for b in self.boards if b.has_won()), None)

    def apply_next_move(self):
        self.last_move = self.moves.pop(0)
        for board in self.boards:
            board.apply_move(self.last_move)

    def get_last_move_called(self) -> int:
        return self.last_move

    def get_remaining_boards(self) -> list[Board]:
        return [b for b in self.boards if not b.has_won()]

def read_game(input_filename: str) -> Game:
    with open(input_filename, encoding="utf-8") as f:
        text_groups = f.read().strip().split("\n\n")
        moves = [int(n) for n in text_groups[0].strip().split(',')]
        boards = [to_board(l) for l in text_groups[1:]]
        return Game(moves, boards)

def to_board(text: str) -> Board:
    return Board([to_row(t) for t in text.split('\n')])

def to_row(text: str) -> Row:
    return Row([int(n) for n in text.split(' ') if n])

def get_winning_board_score(game: Game) -> int:
    while (winning_board := game.get_winning_board()) is None:
        game.apply_next_move()
    return winning_board.get_score() * game.get_last_move_called()


def get_losing_board_score(game: Game) -> int:
    while len(remaining_boards := game.get_remaining_boards()) != 1:
        game.apply_next_move()
    remaining_board = remaining_boards[0]

    while not remaining_board.has_won():
        game.apply_next_move()
    return remaining_board.get_score() * game.get_last_move_called()

GAME = read_game("input/input4.txt")
if __name__ == "__main__":
    print(f"Winning board score {get_winning_board_score(deepcopy(GAME))}")
    print(f"Losing board score {get_losing_board_score(deepcopy(GAME))}")
