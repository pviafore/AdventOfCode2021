from collections import Counter

Rule = tuple[str, str]
Polymers = tuple[str, list[Rule]]
def to_polymers(text: list[str]) -> Polymers:
    start = text[0].strip()
    rules = [t.strip().split(" -> ", 2) for t in text[2:]]
    return (start, rules) # type: ignore

def get_difference_of_most_and_least_common(polymers: Polymers,
                                            times:int=10) -> int:
    start, rules = polymers
    pairs = [l1 + l2 for l1, l2 in zip(start, start[1:])]
    polymer_pairs = Counter(pairs)
    last_pair = pairs[-1]
    for _ in range(times):

        new_polymer_pairs: Counter[str] = Counter()
        for polymer, count in polymer_pairs.items():

            new_pairs = convert_rule(polymer, rules)
            if polymer == last_pair:
                last_pair = new_pairs[-1]
            for pair in new_pairs:
                new_polymer_pairs[pair] += count
        polymer_pairs =  new_polymer_pairs

    all_letters: Counter[str] = Counter()
    for polymer, count in polymer_pairs.items():
        all_letters[polymer[0]] += count
    all_letters[last_pair[-1]] += 1

    return max(all_letters.values()) - min(all_letters.values())


def convert_rule(pair: str, rules: list[Rule]) -> list[str]:
    try:
        matching_rule = next(r for r in rules if r[0] == pair)
        return [pair[0] + matching_rule[1], matching_rule[1] + pair[1]]
    except StopIteration:
        return [pair]



with open("input/input14.txt", encoding="utf-8") as f:
    POLYMERS = to_polymers(f.readlines())

if __name__ == "__main__":
    print(f"Difference: {get_difference_of_most_and_least_common(POLYMERS)}")
    print(f"Difference (40): "
          f"{get_difference_of_most_and_least_common(POLYMERS, times=40)}")
