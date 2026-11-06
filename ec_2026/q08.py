from itertools import cycle

Data = list[str]


def parse(text: str) -> Data:
    return [line.strip() for line in text.splitlines() if line.strip()]


Field = list[list[int | None]]


def get_field(data: Data) -> Field:
    return [[None if cell == "." else int(cell) for cell in line] for line in data]


def grow(field: Field, direction: tuple[int, int]) -> tuple[int, int]:
    dr, dc = direction
    rows, cols = range(len(field)), range(len(field[0]))
    if dr < 0:
        rows = rows[::-1]
        dr = -dr
    if dc < 0:
        cols = cols[::-1]
        dc = -dc
    norm = dr**2 + dc**2

    energy, warriors, shadows = 0, 0, {}
    for row, r in enumerate(rows):
        line = field[r]
        for col, c in enumerate(cols):
            height = line[c]
            if height is None:
                continue

            if height <= 0:
                line[c] += 1
                continue

            rank = dc * row - dr * col
            dist = (dr * row + dc * col) // norm
            if height > shadows.get(rank, 0) - dist:
                energy += 1
                shadows[rank] = height + dist

                if height < 9:
                    line[c] += 1
                else:
                    warriors += 1
                    line[c] = -2

    return energy, warriors


def part1(data: Data) -> int:
    field = get_field(data)
    energy, _ = grow(field, (1, 1))
    return energy


DIRECTIONS = ((1, 1), (1, -1), (0, -2), (-1, -1), (-1, 1), (0, 2))


def part2(data: Data) -> int:
    field = get_field(data)
    total = 0
    for direction in DIRECTIONS:
        energy, _ = grow([line[:] for line in field], direction)
        total += energy
    return total


def part3(data: Data) -> int:
    field = get_field(data)
    total, count = 0, 0
    for direction in cycle(DIRECTIONS):
        energy, warriors = grow(field, direction)
        total += energy
        count += warriors
        if count >= 100_000:
            break

    return total
