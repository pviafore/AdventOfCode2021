from common.file_input import read_multiline

def get_power_rate(numbers: list[str]) -> int:
    bitgroups = zip(*numbers)
    gamma_bitstring = [get_most_common_bit(b) for b in bitgroups]
    gamma_rate = int(''.join(gamma_bitstring), base=2)
    # this is a bit of cheat since we know its 12 bits long
    return gamma_rate * (~gamma_rate & 0xFFF)

def get_most_common_bit(bits: tuple[str, ...], inverse=False) -> str:
    if len(bits) == 1:
        return bits[0]
    if inverse:
        return '0' if bits.count('1') >= bits.count('0') else '1'
    return '1' if bits.count('1') >= bits.count('0') else '0'

def get_life_support_rating(numbers: list[str]) -> int:
    return (get_oxygen_generator_rating(numbers) *
            get_co2_scrubber_rating(numbers))

def get_oxygen_generator_rating(numbers: list[str]) -> int:
    return int(filter_numbers(numbers), base=2)

def get_co2_scrubber_rating(numbers: list[str]) -> int:
    return int(filter_numbers(numbers, inverse=True), base=2)

def filter_numbers(numbers: list[str], inverse=False) -> str:
    for index in range(len(numbers[0])):
        bits = tuple(n[index] for n in numbers)
        numbers = [n for n in numbers if n[index] == get_most_common_bit(bits, inverse=inverse)]
    return numbers[0]

NUMBERS = read_multiline("input/input3.txt")

if __name__ == "__main__":
    print(f"Power rate: {get_power_rate(NUMBERS)}")
    print(f"Life Support Rating: {get_life_support_rating(NUMBERS)}")
