import functools
import itertools
import math
import operator

from copy import deepcopy
from typing import Iterator, Optional, Union

from common.file_input import read_multiline

SnailfishNode = Union[int, 'Snailfish']
class Snailfish:
    def __init__(self, left: SnailfishNode, right: SnailfishNode, reduce=True):
        self.left = left
        self.right = right
        self.parent = None
        if isinstance(self.left, Snailfish):
            self.left.parent = self
        if isinstance(self.right, Snailfish):
            self.right.parent = self
        while reduce and self._reduce():
            pass

    def __add__(self, rhs: 'Snailfish') -> 'Snailfish':
        assert isinstance(rhs, Snailfish)
        return Snailfish(deepcopy(self), deepcopy(rhs))

    def apply_to_node_to_the_left(self, value: int,
                                requesting_child: Optional['Snailfish']=None):
        if isinstance(self.left, int):
            self.left += value
        else:
            if requesting_child == self.right:
                self.left.apply_to_node_to_the_right(value)
            elif requesting_child == self.left:
                parent = self.parent
                child = self
                while parent and parent.left == child:
                    child = parent
                    parent = parent.parent
                if parent is not None:
                    if isinstance(parent.left, int):
                        parent.left += value
                    else:
                        parent.left.apply_to_node_to_the_right(value)
            else: # comes from above
                self.left.apply_to_node_to_the_left(value)

    def apply_to_node_to_the_right(self, value: int,
                                requesting_child: Optional['Snailfish']=None):
        if isinstance(self.right, int):
            self.right += value
        else:
            if requesting_child == self.left:
                self.right.apply_to_node_to_the_left(value)
            elif requesting_child == self.right:
                parent = self.parent
                child = self
                while parent and parent.right == child:
                    child = parent
                    parent = parent.parent
                if parent is not None:
                    if isinstance(parent.right, int):
                        parent.right += value
                    else:
                        parent.right.apply_to_node_to_the_left(value)
            else: # comes from above
                self.right.apply_to_node_to_the_right(value)


    def _reduce(self) -> bool:
        reduced = self.reduce_explode()
        if not reduced:
            reduced = self.reduce_split()
        return reduced

    def reduce_split(self) -> bool:
        reduced = self._reduce_left_split()
        if not reduced:
            reduced = self._reduce_right_split()
        return reduced


    def reduce_explode(self, level=0) -> bool:
        reduced = self._reduce_left_explode(level)
        if not reduced:
            reduced = self._reduce_right_explode(level)
        return reduced

    def _reduce_left_explode(self, level=0) -> bool:
        if isinstance(self.left, Snailfish):
            if level == 3:
                self._explode_left()
                return True
            return self.left.reduce_explode(level + 1)
        return False

    def _reduce_left_split(self) -> bool:
        if isinstance(self.left, int) and self.left >= 10:
            self.left = Snailfish(math.floor(self.left / 2),
                                math.ceil(self.left / 2),
                                reduce=False)
            self.left.parent = self
            return True
        if isinstance(self.left, Snailfish):
            return self.left.reduce_split()
        return False


    def _explode_left(self):
        # nested 4 deep
        assert isinstance(self.left, Snailfish)
        assert isinstance(self.left.right, int)
        assert isinstance(self.left.left, int)
        if isinstance(self.right, int):
            self.right += self.left.right
        else:
            self.apply_to_node_to_the_right(self.left.right, self.left)
        if self.parent is not None:
            self.parent.apply_to_node_to_the_left(self.left.left, self)
        self.left = 0

    def _reduce_right_explode(self, level=0) -> bool:
        if isinstance(self.right, Snailfish):
            if level == 3:
                self._explode_right()
                return True
            return self.right.reduce_explode(level + 1)
        return False

    def _reduce_right_split(self) -> bool:
        if isinstance(self.right, int) and self.right >= 10:
            self.right = Snailfish(math.floor(self.right / 2),
                                math.ceil(self.right / 2),
                                reduce=False)
            self.right.parent = self
            return True
        if isinstance(self.right, Snailfish):
            return self.right.reduce_split()
        return False

    def _explode_right(self):
        assert isinstance(self.right, Snailfish)
        # nested 4 deep
        assert isinstance(self.right.left, int)
        assert isinstance(self.right.right, int)
        if isinstance(self.left, int):
            self.left += self.right.left
        else:
            self.apply_to_node_to_the_left(self.right.left, self.right)
        if self.parent is not None:
            self.parent.apply_to_node_to_the_right(self.right.right, self)
        self.right = 0

    def get_magnitude(self) -> int:
        left_value = (self.left if isinstance(self.left, int)
                                else self.left.get_magnitude())
        right_value = (self.right if isinstance(self.right, int)
                                  else self.right.get_magnitude())
        return 3*left_value + 2*right_value

    def __str__(self) -> str:
        return f"[{self.left},{self.right}]"

def to_snailfish(text: str) -> Snailfish:
    text_iter = iter(text)
    snailfish = parse_snailfish(text_iter)
    try:
        next(text_iter)
        assert False, "Iterator was not exhausted"
    except StopIteration:
        pass
    assert isinstance(snailfish, Snailfish)
    return snailfish

def parse_snailfish(text_iter: Iterator, level=0) -> SnailfishNode:
    left: Optional[SnailfishNode] = None
    right: Optional[SnailfishNode] = None
    try:
        while True:
            char = next(text_iter)
            if char in '1234567890':
                if left is None:
                    left = int(char)
                else:
                    assert right is None
                    right = int(char)
            if char == ',':
                assert left is not None and right is None
            if char == '[':
                snailfish = parse_snailfish(text_iter, level+1)
                if left is None:
                    left = snailfish
                else:
                    assert right is None
                    right = snailfish
            if char == ']':
                assert left is not None and right is not None
                return Snailfish(left, right, reduce=False)
    except StopIteration:
        # only one snailfish at the top
        assert left is not None
        return left

def get_magnitude(snailfish: list[Snailfish]) -> int:
    reduced = functools.reduce(operator.add, snailfish)
    return reduced.get_magnitude()

def get_largest_magnitude(snailfish: list[Snailfish]) -> int:
    pairs = list(itertools.product(snailfish, snailfish))

    return max((s1+s2).get_magnitude() for s1, s2 in pairs if s1 != s2)


SNAILFISH = read_multiline("input/input18.txt", to_snailfish)
if __name__ == "__main__":
    print(f"Magnitude of fish: {get_magnitude(SNAILFISH)}")
    print(f"Largest magnitude: {get_largest_magnitude(SNAILFISH)}")
