from collections import Counter, defaultdict
from collections.abc import Iterable
from heapq import heappop, heappush
from itertools import combinations

Data = list[str]
Graph = dict[str, Counter[str]]


def parse(text: str) -> Data:
    return [line.strip() for line in text.splitlines() if line.strip()]


def get_graph(data: Data) -> Graph:
    graph = defaultdict(Counter)
    for lines in (data, zip(*data, strict=True)):
        for line in lines:
            prev = " "
            for cell in line:
                if cell != prev:
                    graph[cell][prev] += 1
                    graph[prev][cell] += 1
                    prev = cell
            cell = " "
            graph[cell][prev] += 1
            graph[prev][cell] += 1
    return graph


def get_needed_bindings(graph: Graph, charges: Iterable[str] = ()) -> int:
    charged = set(charges)

    def push_edges(prev_piece: str) -> None:
        for next_piece, next_bindings in graph[prev_piece].items():
            if next_piece not in connected:
                # A charge binds every edge of the chosen piece, including this one.
                cost = 0 if prev_piece in charged or next_piece in charged else next_bindings
                heappush(heap, (cost, next_piece))

    connected = {" "}
    heap: list[tuple[int, str]] = []
    push_edges(" ")
    total_bindings = 0
    while heap:
        bindings, piece = heappop(heap)
        if piece in connected:
            continue
        connected.add(piece)
        total_bindings += bindings
        push_edges(piece)
    return total_bindings


def part1(data: Data) -> int:
    graph = get_graph(data)
    return sum(bindings for edges in graph.values() for bindings in edges.values()) // 2


def part2(data: Data) -> int:
    graph = get_graph(data)
    return get_needed_bindings(graph)


def part3(data: Data, charges: int = 2) -> int:
    graph = get_graph(data)
    pieces = set(graph) - {" "}
    return min(get_needed_bindings(graph, charge_pieces) for charge_pieces in combinations(pieces, charges))
