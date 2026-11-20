from collections import Counter
from itertools import permutations
from math import prod

Layer = list[str]
Data = list[Layer]


def parse(text: str) -> Data:
    return [layer.split() for layer in text.strip().split("\n\n")]


COLORS = "CMYK"
RULES = (
    {("K", color): "K" for color in COLORS}
    | {("C", "M"): "B", ("C", "Y"): "G", ("M", "Y"): "R"}
    | {(color, color): color for color in COLORS}
)
RULES |= {(b, a): c for (a, b), c in RULES.items()}


def count_cubes(top_layer: Layer, bottom_layer: Layer) -> int:
    top_colors, bottom_colors = "".join(top_layer), "".join(bottom_layer)
    count = Counter(RULES[pair] for pair in zip(top_colors, bottom_colors, strict=True))
    return prod(n for _, n in count.most_common(3))


def translate(layer: Layer, substitution: dict[str, str]) -> Layer:
    return ["".join(substitution[c] for c in line) for line in layer]


def part1(data: Data) -> int:
    return count_cubes(*data)


def part2(data: Data) -> int:
    top_layer, bottom_layer = data
    best = 0
    for colors in permutations(COLORS):
        substitution = dict(zip("1234", colors, strict=True))
        best = max(best, count_cubes(top_layer, translate(bottom_layer, substitution)))
    return best


def part3(data: Data) -> int:
    layer = data[0]
    count = Counter(c for line in layer for c in line)
    total = sum(count.values()) - count["K"]

    # Split the CMY colors in 3 similar groups
    div, mod = divmod(total, 3)
    max_without_k = prod(div + (i < mod) for i in range(3))

    # Keep the K colors and split the CMY colors in 2 similar groups
    div, mod = divmod(total, 2)
    max_with_k = count["K"] * prod(div + (i < mod) for i in range(2))

    # Both splits are always achievable. Rename so that C >= M >= Y, t = C + M + Y:
    # - 2 groups: B and G (M -> B, Y -> G, C fills either; M, Y <= t/2).
    # - 3 groups: B, G, R if C <= 2t/3 (R filled by M and Y), else C, B, G.

    return max(max_with_k, max_without_k)
