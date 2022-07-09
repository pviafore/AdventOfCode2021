import heapq

from copy import deepcopy
from dataclasses import dataclass

from typing import Generator


@dataclass(frozen=True)
class Room:
    tag: str
    spots: list[str | None]

    def is_complete(self) -> bool:
        return all(s == self.tag for s in self.spots)

    def can_fit(self, amphipod: str) -> bool:
        return (
            all(s is None or s == amphipod for s in self.spots) and
            self.spots[0] is None and
            self.tag == amphipod
        )

    def get_first_filled_spot(self) -> int:
        return next((index for index, spot in enumerate(self.spots)
                     if spot is not None), len(self.spots))

    def with_added_amphipod(self, amphipod: str) -> 'Room':
        assert self.can_fit(amphipod)
        next_spot = self.get_first_filled_spot() - 1
        new_spots = deepcopy(self.spots)
        new_spots[next_spot] = amphipod

        return Room(
            self.tag,
            new_spots
            )

    def with_removed_amphipod(self, amphipod: str) -> 'Room':
        assert self.get_occupant() == amphipod

        next_spot = self.get_first_filled_spot()
        new_spots = deepcopy(self.spots)
        new_spots[next_spot] = None

        return Room(
            self.tag,
            new_spots
        )

    def entry_cost(self) -> int:
        return self.get_first_filled_spot()

    def exit_cost(self) -> int:
        assert not self.is_empty()
        return self.get_first_filled_spot() + 1

    def is_empty(self) -> bool:
        return all(s is None for s in self.spots)

    def get_occupant(self) -> str:
        occupant = self.spots[self.get_first_filled_spot()]
        assert occupant is not None
        return occupant


# this represents the current positioning
Spaces = list[str | Room | None]


# just so we can heapify it
@dataclass(frozen=True)
class Layout:
    spaces: Spaces

    def __lt__(self, rhs: 'Layout'):
        return str(self) < str(rhs)

    def __hash__(self) -> int:
        return hash(str(self))


SPACES: Spaces = [
    None,
    None,
    Room("A", ["C", "D"]),
    None,
    Room("B", ["A", "C"]),
    None,
    Room("C", ["B", "A"]),
    None,
    Room("D", ["D", "B"]),
    None,
    None
]

BIG_SPACES: Spaces = [
    None,
    None,
    Room("A", ["C", "D", "D", "D"]),
    None,
    Room("B", ["A", "C", "B", "C"]),
    None,
    Room("C", ["B", "B", "A", "A"]),
    None,
    Room("D", ["D", "A", "C", "B"]),
    None,
    None
]


def is_complete(spaces: Spaces) -> bool:
    return all(room.is_complete() for room in spaces if isinstance(room, Room))


COSTS = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000
}


def move_amphipod_to_room(spaces: Spaces,
                          from_space: int,
                          to_space: int,
                          amphipod: str) -> tuple[int, Spaces]:
    room = spaces[to_space]
    assert isinstance(room, Room) and room.can_fit(amphipod)

    new_layout = deepcopy(spaces)
    new_layout[from_space] = None
    entry_cost = room.entry_cost()
    new_layout[to_space] = room.with_added_amphipod(amphipod)
    return ((abs(from_space - to_space) + entry_cost) * COSTS[amphipod],
            new_layout)


def move_amphipod_from_room(spaces: Spaces,
                            from_space: int,
                            to_space: int,
                            amphipod: str) -> tuple[int, Spaces]:
    room = spaces[from_space]
    assert isinstance(room, Room)

    new_layout = deepcopy(spaces)
    new_layout[to_space] = amphipod
    exit_cost = room.exit_cost()
    new_layout[from_space] = room.with_removed_amphipod(amphipod)
    return ((abs(from_space - to_space) + exit_cost) * COSTS[amphipod],
            new_layout)


def move_to_room(spaces: Spaces, index: int,
                 destination: int,
                 stride: int) -> Generator[tuple[int, Spaces], None, None]:
    amphipod = spaces[index]
    assert isinstance(amphipod, str)

    for to_space in range(index, destination+stride, stride):
        spot = spaces[to_space]
        if isinstance(spot, str) and to_space != index:
            # found another amphipod
            break
        if isinstance(spot, Room):
            if spot.can_fit(amphipod):
                yield move_amphipod_to_room(spaces, index,
                                            to_space, amphipod)


def move_to_hallway(spaces: Spaces, index: int,
                    destination: int,
                    stride: int) -> Generator[tuple[int, Spaces], None, None]:
    room = spaces[index]
    assert isinstance(room, Room)
    if room.is_empty():
        return

    for to_space in range(index, destination + stride, stride):
        spot = spaces[to_space]
        if isinstance(spot, str):
            # found another amphipod
            break
        if spot is None:
            yield move_amphipod_from_room(spaces, index, to_space,
                                          room.get_occupant())


# get the solution space for possible moves
def get_possible_moves(spaces: Spaces) -> Generator[tuple[int, Spaces],
                                                    None, None]:
    for index, space in enumerate(spaces):
        # get hallway to room moves
        if isinstance(space, str):
            # start walking back and forth until you find an empty room
            yield from move_to_room(spaces, index, 0, -1)
            yield from move_to_room(spaces, index, len(spaces) - 1, 1)
        # get room to hallway moves
        if isinstance(space, Room):
            yield from move_to_hallway(spaces, index, 0, -1)
            yield from move_to_hallway(spaces, index, len(spaces) - 1, 1)


def get_minimum_energy(spaces: Spaces) -> int:
    states = [(0, Layout(spaces))]
    seen = set([states[0][1]])
    while states:
        cost, candidate = heapq.heappop(states)
        if is_complete(candidate.spaces):
            return cost
        for new_cost, new_spaces in get_possible_moves(candidate.spaces):
            layout = Layout(new_spaces)
            if layout in seen:
                continue
            seen.add(layout)
            heapq.heappush(states, (cost + new_cost, layout))
    assert False, "Should never reach here"


if __name__ == "__main__":
    print(f"Minimum energy: {get_minimum_energy(SPACES)}")
    print(f"Minimum energy (Big Spaces): {get_minimum_energy(BIG_SPACES)}")
