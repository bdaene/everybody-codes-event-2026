"""Copy to ec_2026/qNN.py. Add part2/part3 (or alias them) as they unlock."""

Data = list[str]


def parse(text: str) -> Data:
    # Drops blank lines: adapt if the input uses them to separate sections.
    return [line.strip() for line in text.splitlines() if line.strip()]


def part1(data: Data) -> int:
    raise NotImplementedError
