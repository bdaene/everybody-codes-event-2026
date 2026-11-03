from itertools import count
from pathlib import Path

Data = list[int]


def parse_data(path: Path) -> Data:
    return [int(number) for number in path.read_text().strip().split(',')]


def run(data: Data, part: int) -> int:
    if part == 1:
        sequence = (i ** 2 for i in count(1))
    elif part == 2:
        sequence = (4 * i for i in count(2))
    elif part == 3:
        sequence = (i ** 2 - 1 for i in count(3, 2))
    else:
        raise ValueError('Invalid part number')

    pattern = next(sequence)
    total = 0
    for number in data:
        while pattern < number:
            pattern = next(sequence)
        total += pattern - number

    return total
