from collections.abc import Iterable
from itertools import count
from pathlib import Path


def parse_data(path: Path):
    with open(path) as f:
        return [int(number) for number in f.readline().strip().split(',')]

def run(data: Iterable[int],  part: int = 1) -> int:
    if part == 1:
        sequence = (i**2 for i in count(1))
    elif part == 2:
        sequence = (4*i for i in count(2))
    elif part == 3:
        sequence = (i**2-1 for i in count(3,2))
    else:
        raise ValueError('Invalid part number')

    pattern = next(sequence)
    total = 0
    for number in data:
        while pattern < number:
            pattern = next(sequence)
        total += pattern - number

    return total

