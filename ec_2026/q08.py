from itertools import cycle

Data = list[str]


def parse(text: str) -> Data:
    return [line.strip() for line in text.splitlines() if line.strip()]


DIRECTIONS = ((1, 1), (1, -1), (0, -2), (-1, -1), (-1, 1), (0, 2))

Field = list[int]
Lines = list[list[int]]


def get_field(data: Data) -> tuple[Field, list[Lines]]:
    field, indices = [], {}
    for r, line in enumerate(data):
        for c, cell in enumerate(line):
            if cell != ".":
                indices[r, c] = len(field)
                field.append(int(cell))

    plans = []
    for dr, dc in DIRECTIONS:
        plan = []
        for r, c in indices:
            if (r - dr, c - dc) in indices:
                continue  # Not the start of a line
            line = []
            while (r, c) in indices:
                line.append(indices[r, c])
                r, c = r + dr, c + dc
            plan.append(line)
        plans.append(plan)

    return field, plans


def grow(field: Field, plan: Lines) -> tuple[int, int]:
    energy, warriors = 0, 0
    for line in plan:
        shadow = 0
        for i in line:
            shadow -= 1
            height = field[i]
            if height <= 0:
                field[i] += 1
                continue
            if height > shadow:
                energy += 1
                shadow = height
                if height < 9:
                    field[i] += 1
                else:
                    warriors += 1
                    field[i] = -2

    return energy, warriors


def part1(data: Data) -> int:
    field, plans = get_field(data)
    energy, _ = grow(field, plans[0])
    return energy


def part2(data: Data) -> int:
    field, plans = get_field(data)
    return sum(grow(field[:], plan)[0] for plan in plans)


def part3(data: Data) -> int:
    field, plans = get_field(data)
    total, count = 0, 0
    for plan in cycle(plans):
        energy, warriors = grow(field, plan)
        total += energy
        count += warriors
        if count >= 100_000:
            break

    return total
