from collections.abc import Generator

Link = tuple[int, int]
Data = tuple[int, list[Link]]


def parse(text: str) -> Data:
    lines = text.splitlines()
    portals = int(lines[0].removeprefix("portals: "))

    links = []
    for line in lines[2:]:
        line = line.strip()
        if not line:
            continue
        a, b = map(int, line.split())
        links.append((a - 1, b - 1))

    return portals, links


def reduce_distances(distances: list[list[int]]):
    n = len(distances)
    for c in range(n):
        for a in range(n):
            for b in range(n):
                distances[a][b] = min(distances[a][b], distances[a][c] + distances[c][b])


def add_link(distances, a, b):
    n = len(distances)
    for i in range(n):
        for j in range(n):
            distances[i][j] = min(
                distances[i][j],
                distances[i][a] + 1 + distances[b][j],
                distances[i][b] + 1 + distances[a][j],
            )


def get_total(distances) -> int:
    return sum(sum(line) for line in distances)


def prepare_distances(portals, links, reach: int = 3) -> tuple[list[list[int]], int]:
    distances = [[portals for b in range(portals)] for a in range(portals)]
    for a in range(portals):
        distances[a][a] = 0
        for b in range(a + 1, a + 1 + reach):
            distances[a][b % portals] = 1
            distances[b % portals][a] = 1
    reduce_distances(distances)
    initial_strain = get_total(distances)

    for a, b in links:
        add_link(distances, a, b)

    return distances, initial_strain


def part1(data: Data) -> int:
    portals, links = data

    distances, initial_strain = prepare_distances(portals, links, reach=1)
    final_strain = get_total(distances)

    return initial_strain - final_strain


def part2(data: Data) -> int:
    portals, links = data

    distances, initial_strain = prepare_distances(portals, links, reach=3)

    a, b = max(((a, b) for a in range(portals) for b in range(a)), key=lambda ab: distances[ab[0]][ab[1]])
    add_link(distances, a, b)
    final_strain = get_total(distances)

    return initial_strain - final_strain


def gen_links(nodes: list[int]) -> Generator[tuple[Link, ...]]:
    if not nodes:
        yield ()
        return

    a = nodes.pop()
    for i in range(len(nodes)):
        b = nodes.pop(i)
        for links in gen_links(nodes):
            yield (a, b), *links
        nodes.insert(i, b)
    nodes.append(a)


def part3(data: Data) -> int:
    portals, links = data

    distances, initial_strain = prepare_distances(portals, links, reach=3)
    best = get_total(distances)

    spread = portals // 8
    for a in range(spread):
        nodes = [a + spread * i for i in range(8)]
        for new_links in gen_links(nodes):
            distances_ = [row[:] for row in distances]
            for link in new_links:
                add_link(distances_, *link)

            strain = get_total(distances_)
            if strain < best:
                best = strain

    return initial_strain - best
