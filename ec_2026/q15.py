from dataclasses import dataclass
from heapq import heappop, heappush

Data = list[str]


def parse(text: str) -> Data:
    return [line.strip() for line in text.splitlines() if line.strip()]


@dataclass
class Arc:
    start: int
    end: int
    height: int
    sulphur: int

    @property
    def length(self) -> int:
        return self.end - self.start + self.height * 2


def parse_arcs(data: Data) -> list[Arc]:
    rows = len(data)
    assert data[rows // 2][0] == "S"
    assert data[rows // 2][-1] == "E"

    ends, arcs = set(), []
    for col, cell in enumerate(data[rows // 2 - 1]):
        if cell != "#" and col not in ends:
            count = 0
            row = rows // 2 - 1
            start = col
            while data[row][col] != "#":
                count += data[row][col] == "@"
                row -= 1
            row += 1
            height = rows // 2 - row
            col += 1
            while data[row][col] != "#":
                count += data[row][col] == "@"
                col += 1
            col -= 1
            row += 1
            while row < rows // 2:
                count += data[row][col] == "@"
                row += 1
            arcs.append(Arc(start, col, height, count))
            ends.add(start)
            ends.add(col)

    ends = set()
    for col, cell in enumerate(data[rows // 2 + 1]):
        if cell != "#" and col not in ends:
            count = 0
            row = rows // 2 + 1
            start = col
            while data[row][col] != "#":
                count += data[row][col] == "@"
                row += 1
            row -= 1
            height = row - rows // 2
            col += 1
            while data[row][col] != "#":
                count += data[row][col] == "@"
                col += 1
            col -= 1
            row -= 1
            while row > rows // 2:
                count += data[row][col] == "@"
                row -= 1
            arcs.append(Arc(start, col, height, count))
            ends.add(start)
            ends.add(col)

    return arcs


def search(arcs: list[Arc], start: int, end: int, needed_sulphur: int) -> int:

    heap: list[tuple[int, int, int, int | None, int, dict[tuple[int, int], tuple[int, int]]]] = [
        (end - start, needed_sulphur, start, None, 0, {})
    ]

    seen = {}
    while heap:
        steps, needed_sulphur, position, last_arc_id, _, path = heappop(heap)
        if needed_sulphur == 0:
            return steps
        if needed_sulphur < 0:
            continue
        if last_arc_id is not None:
            key = (position, last_arc_id)
            if key in seen:
                if seen[key] <= (needed_sulphur, steps):
                    continue
            # print(steps, needed_sulphur, position, last_arc_id, path)
            if key in path:
                # Skip ahead
                prev_sulphur, prev_steps = path[key]
                loops = (needed_sulphur - 1) // (prev_sulphur - needed_sulphur)
                if loops > 0:
                    heappush(
                        heap,
                        (
                            steps + loops * (steps - prev_steps),
                            needed_sulphur - loops * (prev_sulphur - needed_sulphur),
                            position,
                            last_arc_id,
                            id(path),
                            path,
                        ),
                    )
                    continue

            seen[key] = (needed_sulphur, steps)
            path = path | {key: (needed_sulphur, steps)}

            last_arc = arcs[last_arc_id]
            heappush(
                heap,
                (
                    steps + last_arc.length + last_arc.end - last_arc.start,
                    needed_sulphur - last_arc.sulphur,
                    position,
                    last_arc_id,
                    id(path),
                    path,
                ),
            )

        steps -= end - position
        for arc_id, arc in enumerate(arcs):
            if arc_id == last_arc_id:
                continue
            heappush(
                heap,
                (
                    steps + arc.length + abs(arc.start - position) + end - arc.end,
                    needed_sulphur - arc.sulphur,
                    arc.end,
                    arc_id,
                    id(path),
                    path,
                ),
            )
            heappush(
                heap,
                (
                    steps + arc.length + abs(arc.end - position) + end - arc.start,
                    needed_sulphur - arc.sulphur,
                    arc.start,
                    arc_id,
                    id(path),
                    path,
                ),
            )

    raise RuntimeError


def part1(data: Data) -> int:
    # Pen and paper
    return 184


def part2(data: Data) -> int:
    arcs = [arc for arc in parse_arcs(data) if arc.sulphur > 0]
    return search(arcs, 0, len(data[0]) - 1, 2026)


def part3(data: Data) -> int:
    arcs = [arc for arc in parse_arcs(data) if arc.sulphur > 0]
    return search(arcs, 0, len(data[0]) - 1, 202620262026)
