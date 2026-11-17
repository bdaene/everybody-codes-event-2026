Data = str


def parse(text: str) -> Data:
    return text.strip()


def flip(line: str) -> tuple[int, int, str]:
    if not line:
        return 0, 0, ""

    sep = line[0]
    start, end, right = 0, len(line) - 1, ""
    while start != end and line[start] == sep:
        start += 1
    while start != end and (c := line[end]) != sep:
        right += c
        end -= 1

    direction, count, total = 1, 0, 0
    while start != end:
        direction = -direction
        start, end = end, start
        count += 1
        total += 1 + abs(end - start)

        while start != end and line[start] == sep:
            start += direction
        while start != end and (c := line[end]) != sep:
            right += c
            end -= direction

    if line[start] != sep:
        right += line[start]
    return count, total, right[::-1]


def part1(data: Data) -> int:
    total = 0

    right = data
    while right:
        flips, _, right = flip(right)
        total += flips

    return total


def part2(data: Data, factor=10) -> int:
    total = 0

    right = data * factor
    while right:
        _, count, right = flip(right)
        total += count

    return total


def part3(data: Data, factor=100) -> int:
    return part2(data, factor)
