from dataclasses import dataclass


@dataclass
class Plant:
    id: int
    growth: int
    limit: int


Data = list[Plant]


def parse(text: str) -> Data:
    plants = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        values = {key: int(value) for key, value in (item.split("=") for item in line.split(", "))}
        plants.append(Plant(**values))

    return plants


def grow(growth: int, limit: int) -> int:
    branches, splits, time = {1: 1}, 0, 1
    while sum(size * n for size, n in branches.items()) + splits < limit:
        time += 1

        branches = {size + 1: n for size, n in branches.items()}
        n = branches.pop(growth, 0)
        splits += n
        branches[1] = branches.get(1, 0) + n
        branches[growth // 2] = branches.get(growth // 2, 0) + 2 * n

    return time


def part1(data: Data) -> int:
    return sum(grow(plant.growth, plant.limit) for plant in data)


def grow_fast(growth: int, limit: int) -> int:
    branches, splits, time = {1: 1}, 0, 1
    while splits + 1 < limit:
        time_to_split = growth - max(branches)
        time += time_to_split

        branches = {size + time_to_split: n for size, n in branches.items()}
        n = branches.pop(growth, 0)
        splits += n
        branches[1] = branches.get(1, 0) + n
        branches[growth // 2] = branches.get(growth // 2, 0) + 2 * n

    return time


def part2(data: Data) -> int:
    return sum(grow_fast(plant.growth, plant.limit) for plant in data)


part3 = part2
