from collections.abc import Iterator
from itertools import count

Data = list[int]


def parse(text: str) -> Data:
    return [int(number) for number in text.strip().split(",")]


def solve(data: Data, sequence: Iterator[int]) -> int:
    pattern = next(sequence)
    total = 0
    for number in sorted(data):
        while pattern < number:
            pattern = next(sequence)
        total += pattern - number

    return total


def part1(data: Data) -> int:
    return solve(data, (i**2 for i in count(1)))


def part2(data: Data) -> int:
    return solve(data, (4 * (i - 1) for i in count(3)))


def part3(data: Data) -> int:
    return solve(data, (i**2 - 1 for i in count(3, 2)))
