from collections import Counter
from collections.abc import Generator

Pos = tuple[int, int]
Shape = set[Pos]
Data = set[Pos]

NEIGHBORS = ((0, 1), (1, 0), (0, -1), (-1, 0))


def parse(text: str) -> Data:
    return {(row, col) for row, line in enumerate(text.splitlines()) for col, cell in enumerate(line) if cell == "#"}


def extract_shapes(cells: Data) -> Generator[Shape]:
    remaining = set(cells)
    while remaining:
        start = remaining.pop()
        shape = {start}
        to_visit = [start]
        while to_visit:
            row, col = to_visit.pop()
            for dr, dc in NEIGHBORS:
                neighbor = row + dr, col + dc
                if neighbor in remaining:
                    remaining.remove(neighbor)
                    shape.add(neighbor)
                    to_visit.append(neighbor)
        yield shape


def get_min_lines(shape: Shape) -> int:
    """Minimum lines for a rectangle with one rectangular hole."""
    rows: list[int] = []
    cols: list[int] = []
    for row, col in shape:
        rows.append(row)
        cols.append(col)

    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    height, width = max_row - min_row + 1, max_col - min_col + 1

    if len(shape) == height * width:  # No hole
        return min(height, width)

    hole_rows = [row for row, count in  Counter(rows).items() if count < width]
    hole_cols = [col for col, count in Counter(cols).items() if count < height]
    min_row_hole, max_row_hole = min(hole_rows), max(hole_rows)
    min_col_hole, max_col_hole = min(hole_cols), max(hole_cols)

    top, bottom = min_row_hole - min_row, max_row - max_row_hole
    left, right = min_col_hole - min_col, max_col - max_col_hole
    inner_height, inner_width = height - top - bottom, width - left - right

    return min(
        height + inner_height,  # Cover with only horizontal lines
        width + inner_width,  # Cover with only vertical lines
        top + bottom + left + right,  # Cover each side in its orientation
        height + left,  # Cover horizontally 3 sides and vertically the last one
        height + right,
        width + top,  # Cover vertically 3 sides and horizontally the last one
        width + bottom,
    )


def part3(data: Data) -> int:
    return sum(get_min_lines(shape) for shape in extract_shapes(data))


# Parts 1 and 2 are subsets of part 3's shape families.
part1 = part2 = part3
