from collections import defaultdict
from common.file_input import read_multiline


def to_path(text: str) -> tuple[str, str]:
    start, end = text.split('-')
    return start, end


def get_number_of_distinct_paths(paths: list[tuple[str, str]]) -> int:
    graph = build_graph(paths)
    candidates: list[tuple[str, set[str]]] = [("start", set())]
    counter = 0
    while candidates:
        node, seen = candidates.pop(-1)
        if node == 'end':
            counter += 1
            continue
        if node.islower():
            seen = set(seen)
            seen.add(node)
        candidates += [(n, seen) for n in graph[node] if n not in seen]
    return counter


def get_number_of_modified_paths(paths: list[tuple[str, str]]) -> int:
    graph = build_graph(paths)
    candidates: list[tuple[str, set[str], bool]] = [("start", set(), False)]
    counter = 0
    while candidates:
        node, seen, visited_twice = candidates.pop(-1)
        if node == 'end':
            counter += 1
            continue
        if node.islower():
            seen = set(seen)
            seen.add(node)
        for n in graph[node]:
            if n not in seen:
                candidates.append((n, seen, visited_twice))
            elif not visited_twice and n not in ['start', 'end']:
                candidates.append((n, seen, True))
    return counter


def build_graph(paths: list[tuple[str, str]]) -> dict[str, list[str]]:
    graph = defaultdict(list)
    for start, end in paths:
        graph[start].append(end)
        graph[end].append(start)
    return graph


PATHS = read_multiline("input/input12.txt", to_path)

if __name__ == "__main__":
    print(f"Number of distinct paths: {get_number_of_distinct_paths(PATHS)}")
    print(f"Number of distinct paths (single cave twice): "
          f"{get_number_of_modified_paths(PATHS)}")
