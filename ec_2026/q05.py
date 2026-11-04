from collections.abc import Callable, Generator, Iterable
from itertools import product

Data = list[str]


def parse(text: str) -> Data:
    return [line.strip() for line in text.splitlines() if line.strip()]


Pos = tuple[int, int]
Shape = tuple[int, int]


class Grid:
    def __init__(self, rows: list[str]):
        self.rows = [list(row) for row in rows]
        self.shape: Shape = len(self.rows), len(self.rows[0])

    def __str__(self) -> str:
        return "\n".join("".join(row) for row in self.rows)

    def contains(self, pos: Pos) -> bool:
        row, col = pos
        m, n = self.shape
        return 0 <= row < m and 0 <= col < n

    def neighbours(self, pos: Pos, check: bool = True) -> Generator[Pos]:
        row, col = pos
        for dr, dc in product((-1, 0, 1), repeat=2):
            if dr == 0 and dc == 0:
                continue
            n_pos = row + dr, col + dc
            if not check or self.contains(n_pos):
                yield n_pos

    def count_neighbours(self, pos: Pos, values: str) -> int:
        return sum(self.get(n_pos) in values for n_pos in self.neighbours(pos))

    def center(self) -> Pos:
        m, n = self.shape
        return m // 2, n // 2

    def get(self, pos: Pos) -> str:
        row, col = pos
        return self.rows[row][col] if self.contains(pos) else "."

    def set(self, pos: Pos, value: str) -> None:
        row, col = pos
        self.rows[row][col] = value

    def count_cells(self, value: str) -> int:
        return sum(row.count(value) for row in self.rows)

    def cells(self) -> Generator[tuple[Pos, str]]:
        for row, line in enumerate(self.rows):
            for col, cell in enumerate(line):
                yield (row, col), cell


def grow(
    grid: Grid, seeds: Iterable[Pos], value: str, can_grow: Callable[[Pos], bool], years: int | None = None
) -> None:
    new_cells = set(seeds)
    for pos in new_cells:
        grid.set(pos, value)

    year = 0
    while new_cells and (years is None or year < years):
        candidates = {n_pos for pos in new_cells for n_pos in grid.neighbours(pos)}
        new_cells = {pos for pos in candidates if can_grow(pos)}
        for pos in new_cells:
            grid.set(pos, value)
        year += 1


def cover_land(grid: Grid, *, threshold: int = 5) -> None:
    grow(
        grid,
        [grid.center()],
        "#",
        lambda pos: grid.get(pos) != "#" and grid.count_neighbours(pos, "1#") >= threshold,
    )

    for pos, cell in grid.cells():
        if cell != "#":
            grid.set(pos, ".")


def cover_water(grid: Grid, *, threshold: int = 5) -> None:
    grow(
        grid,
        [
            pos
            for pos, cell in grid.cells()
            if cell == "#" and any(grid.get(n_pos) == "." for n_pos in grid.neighbours(pos, check=False))
        ],
        "=",
        lambda pos: grid.get(pos) == "#" and grid.count_neighbours(pos, "=") >= threshold,
    )


def get_pattern(pos: Pos) -> Generator[Pos]:
    row, col = pos
    for dr, dc in product(range(-2, 3), repeat=2):
        if abs(dr) == 2 and abs(dc) == 2:
            continue
        yield row + dr, col + dc


def cover_trees(grid: Grid, *, threshold: int = 4, years: int | None = None) -> None:
    grow(
        grid,
        [pos for pos, _ in grid.cells() if all(grid.get(n_pos) == "#" for n_pos in get_pattern(pos))],
        "@",
        lambda pos: (
            grid.get(pos) == "#"
            and grid.count_neighbours(pos, "@") >= threshold
            and not grid.count_neighbours(pos, "=")
        ),
        years,
    )


def part1(data: Data) -> int:
    grid = Grid(data)
    cover_land(grid)
    return grid.count_cells("#")


def part2(data: Data) -> int:
    grid = Grid(data)
    cover_land(grid)
    cover_water(grid)
    return grid.count_cells("=")


def part3(data: Data) -> int:
    grid = Grid(data)
    cover_land(grid)
    cover_water(grid)
    cover_trees(grid, years=2)
    return grid.count_cells("@")
