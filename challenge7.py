from common.file_input import read_single_line

def get_fuel_spent(crabs: list[int], geometric=False) -> int:
    average_position = sum(crabs) // len(crabs)
    fuel= [calculate_fuel_spent(crabs, average_position - 1, geometric),
           calculate_fuel_spent(crabs, average_position, geometric),
           calculate_fuel_spent(crabs, average_position + 1, geometric)]
    if min(fuel) == fuel[1]:
        return fuel[1]
    step = -1 if fuel[0] < fuel[1] else 1
    pos = average_position + step
    min_fuel = fuel[1 + step]
    while (next_fuel := calculate_fuel_spent(crabs, pos)) <= min_fuel:
        pos = pos + step
        min_fuel = next_fuel

    return min_fuel

def calculate_fuel_spent(crabs: list[int], pos: int, geometric=False) -> int:

    func = (lambda c: sum(range(1, abs(c - pos) + 1))) if geometric else (lambda c: abs(c - pos))
    return sum(func(c) for c in crabs)

CRABS = read_single_line("input/input7.txt", func=int)

if __name__ == "__main__":
    print(f"Fuel spent: {get_fuel_spent(CRABS)}")
    print(f"Fuel spent (geometric): {get_fuel_spent(CRABS, True)}")
