import itertools
import operator

from collections import Counter
from functools import cache
from typing import Iterator

PLAYER1 = 4
PLAYER2 = 2


def get_losing_score_x_dice_rolls(player1: int, player2: int) -> int:
    dice = iter(itertools.cycle(range(1, 101)))
    p1_score, p2_score, dice_rolled = play_until(player1, player2, dice, 1000)
    return dice_rolled * min(p1_score, p2_score)


def get_possibilities_of_roll() -> Counter[int]:
    dice = range(1, 4)
    return Counter(sum(d) for d in itertools.product(dice, dice, dice))


POSSIBILITIES = get_possibilities_of_roll()


def play_until(player1: int, player2: int, dice: Iterator,
               score: int) -> tuple[int, int, int]:
    p1_score = 0
    p2_score = 0
    dice_rolled = 0
    while p1_score < 1000 and p2_score < 1000:
        die_total = next(dice) + next(dice) + next(dice)
        dice_rolled += 3
        points = (player1 + die_total) % 10
        if points == 0:
            points = 10
        player1 = points
        p1_score += player1
        if p1_score >= score:
            break

        die_total = next(dice) + next(dice) + next(dice)
        dice_rolled += 3
        points = (player2 + die_total) % 10
        if points == 0:
            points = 10
        player2 = points
        p2_score += player2

    return (p1_score, p2_score, dice_rolled)


# p1 space, score, p2 space, score, is_player1 -> # of ways to get there
Table = dict[tuple[int, int, int, int, bool], int]


def get_number_of_universes_won_by_predominant_player(player1: int,
                                                      player2: int) -> int:
    table = get_table_scores(player1, player2)
    p1_wins = get_wins(table, 1)
    p2_wins = get_wins(table, 2)
    return max(p1_wins, p2_wins)


def get_wins(table: Table, player: int):
    winner_func = operator.gt if player == 1 else operator.lt
    return sum(ways
               for (p1_score, p2_score, _, __, ___), ways in table.items()
               if winner_func(p1_score, p2_score) and
                (p1_score >= 21 or p2_score >= 21))


def get_table_scores(player1, player2) -> Table:
    table: Table = {}
    # you can have a score from 0 to 30, and on space 1 to 11
    for values in itertools.product(
            range(0, 31),
            range(0, 31),
            range(1, 11),
            range(1, 11),
            [True, False]):
        p1_score, p2_score, p1_space, p2_space, is_player1 = values

        table[values] = get_ways_to_end((player1, p1_score, p1_space),
                                        (player2, p2_score, p2_space),
                                        is_player1)
    return table


Player = tuple[int, int, int]
@cache
def get_ways_to_end(player1: Player, player2: Player,
                    is_player1: bool) -> int:
    _, p1_score, _ = player1
    _, p2_score, _ = player2
    if is_invalid_player_state(player1, player2, is_player1):
        return 0

    # if we have zero score (earlier condition made sure that we're on
    # starting spaces)
    if p1_score == 0 and p2_score == 0:
        return 1

    # loop over all the ways you could have gotten here
    return sum(ways * get_ways_to_roll(player1, player2, is_player1, roll)
               for roll, ways in POSSIBILITIES.items())


def is_invalid_player_state(player1: Player, player2: Player,
                            is_player1: bool) -> bool:
    p1_starting, p1_score, p1_space = player1
    p2_starting, p2_score, p2_space = player2
    # no way for the player to have zero score and not be on starting space
    # also player1 has to move first
    if p1_score == 0 and p1_space != p1_starting:
        return True

    # no way for the player to have zero score and not be on starting space
    if p2_score == 0 and p2_space != p2_starting:
        return True
    # don't let player 1 have zero score if they've already moved
    if p1_score == 0 and is_player1:
        return True
    opposing_player_score = p2_score if is_player1 else p1_score
    # no way for opposition to have above 21 and you have a turn
    if opposing_player_score >= 21:
        return True

    if p1_score < 0 or p2_score < 0:
        return True

    return False




def get_ways_to_roll(player1: Player, player2: Player,
                     is_player1: bool, roll: int) -> int:
    p1_starting, p1_score, p1_space = player1
    p2_starting, p2_score, p2_space = player2
    # subtract your current points
    if is_player1:
        p1_score = p1_score - p1_space
        p1_space -= roll
        if p1_space <= 0:
            p1_space += 10
    else:
        p2_score = p2_score - p2_space
        p2_space -= roll
        if p2_space <= 0:
            p2_space += 10

    return get_ways_to_end((p1_starting, p1_score, p1_space),
                           (p2_starting, p2_score, p2_space),
                           not is_player1)


if __name__ == "__main__":
    print(f"Score x Dice: {get_losing_score_x_dice_rolls(PLAYER1, PLAYER2)}")
    universes_won = get_number_of_universes_won_by_predominant_player(PLAYER1,
                                                                      PLAYER2)
    print(f"Winning Player # of Universes: {universes_won}")
