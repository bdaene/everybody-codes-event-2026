from collections.abc import Generator, Sequence

Pos = tuple[int, int]
Corner = tuple[int, int]
Data = list[str]

DIRECTIONS = ((0, 1), (-1, 0), (0, -1), (1, 0))
# From corner (row, col) — the top-left corner of cell (row, col) — the cell on the
# right-hand side of the edge going in DIRECTIONS[i] is at (row, col) + OFFSETS[i].
OFFSETS = ((0, 0), (-1, 0), (-1, -1), (0, -1))


def parse(text: str) -> Data:
    return [line.strip() for line in text.splitlines() if line.strip()]


class Grid[T]:
    def __init__(self, lines: Sequence[str], ground: str = "#"):
        self.lines = lines
        self.height = len(lines)
        self.width = len(lines[0])
        self.ground = ground

    def is_ground(self, pos: Pos) -> bool:
        row, col = pos
        return 0 <= row < self.height and 0 <= col < self.width and self.lines[row][col] == self.ground

    def gen_neighbors(self, pos: Pos) -> Generator[Pos]:
        row, col = pos
        for dr, dc in DIRECTIONS:
            neighbor = (row + dr, col + dc)
            if self.is_ground(neighbor):
                yield neighbor

    def is_border(self, corner: Corner, direction: int) -> bool:
        """Whether the edge from corner in direction has a ground cell on its right."""
        row, col = corner
        row_offset, col_offset = OFFSETS[direction]
        return self.is_ground((row + row_offset, col + col_offset))

    def perimeter(self) -> int:
        return sum(
            4 - sum(1 for _ in self.gen_neighbors((row, col)))
            for row, line in enumerate(self.lines)
            for col, cell in enumerate(line)
            if cell == self.ground
        )


def get_distance(grid: Grid, start: Pos, end: Pos) -> int:
    seen, to_visit, distance = {start}, [start], 0
    while to_visit:
        next_to_visit = []
        for pos in to_visit:
            if pos == end:
                return distance
            for neighbor in grid.gen_neighbors(pos):
                if neighbor not in seen:
                    seen.add(neighbor)
                    next_to_visit.append(neighbor)
        to_visit = next_to_visit
        distance += 1

    raise ValueError(f"{end} is not reachable from {start}")


def part1(data: Data) -> int:
    grid = Grid(data)
    return get_distance(grid, (0, 0), (grid.height - 1, grid.width - 1))


def part2(data: Data) -> int:
    grid = Grid(data)
    return grid.perimeter()


def part3(data: Data) -> int:
    grid = Grid(data)
    # Follow the border keeping ground on the right, from the top-left corner of the
    # grid to its bottom-right corner, then take the shorter side of the loop.
    start, end = (0, 0), (grid.height, grid.width)
    corner, direction = start, 0

    steps = 0
    while corner != end:
        if not grid.is_border(corner, direction):
            direction = (direction - 1) % 4
            continue
        if grid.is_border(corner, (direction + 1) % 4):
            direction = (direction + 1) % 4
            continue

        dr, dc = DIRECTIONS[direction]
        corner = corner[0] + dr, corner[1] + dc
        steps += 1
        if (corner, direction) == (start, 0):
            raise ValueError(f"{end} is not on the border reachable from {start}")

    return min(steps, grid.perimeter() - steps)
