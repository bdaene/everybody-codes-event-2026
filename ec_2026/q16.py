"""Copy to ec_2026/qNN.py. Add part2/part3 (or alias them) as they unlock."""

Data = str


def parse(text: str) -> Data:
    return text.strip()


def flip(line: str) -> tuple[int, int, str, str]:
    if not line:
        return 0, 0, line, ""

    sep = line[0]
    i, j, left, right = 0, len(line) - 1, "", ""
    while i <= j and (c := line[i]) == sep:
        left += c
        i += 1

    if i >= j:
        return 0, 0, left, ""

    f, count, total = True, 0, 0
    while i <= j:
        if f:
            while i <= j and (c := line[j]) != sep:
                right += c
                j -= 1
            if i <= j:
                total += j - i + 1
            while i <= j and (c := line[j]) == sep:
                left += c
                j -= 1
        else:
            while i <= j and (c := line[i]) != sep:
                right += c
                i += 1
            if i <= j:
                total += j - i + 1
            while i <= j and (c := line[i]) == sep:
                left += c
                i += 1
        f = not f
        count += 1

    return count - 1, total, left, right[::-1]


def part1(data: Data) -> int:
    total = 0

    right = data
    while right:
        flips, _, left, right = flip(right)
        total += flips

    return total


def part2(data: Data, factor=10) -> int:
    total = 0

    right = data * factor
    while right:
        _, count, left, right = flip(right)
        total += count

    return total


def part3(data: Data, factor=100) -> int:
    return part2(data, factor)
