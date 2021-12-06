from collections import Counter

from common.file_input import read_single_line

def get_lanternfish_after(fish: list[int], days: int) -> int:
    counter = Counter(fish)
    for _ in range(days):
        counter = reproduce_fish(counter)
    return sum(counter.values())

def reproduce_fish(counter: Counter) -> Counter:
    new_counter: Counter = Counter()
    for fish, number in counter.items():
        if fish > 0:
            new_counter[fish-1] = number
    if 0 in counter:
        new_counter[6] += counter[0]
        new_counter[8] = counter[0]
    return new_counter


LANTERNFISH = read_single_line("input/input6.txt", func=int)

if __name__ == "__main__":
    print(f"Lanternfish after 80 days: "
          f"{get_lanternfish_after(LANTERNFISH, days=80)}")
    print(f"Lanternfish after 256 days: "
          f"{get_lanternfish_after(LANTERNFISH, days=256)}")
