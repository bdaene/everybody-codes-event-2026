Link = tuple[int, int]
Data = tuple[int, list[Link]]
Distances = list[list[int]]


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


def reduce_distances(distances: Distances) -> None:
    n = len(distances)
    for c in range(n):
        for a in range(n):
            for b in range(n):
                distances[a][b] = min(distances[a][b], distances[a][c] + distances[c][b])


def add_link(distances: Distances, link: Link) -> None:
    a, b = link
    distances_a, distances_b = distances[a], distances[b]
    for i, distances_i in enumerate(distances):
        d_ai, d_bi = distances_a[i], distances_b[i]
        distances[i] = list(
            map(
                min,
                distances_i,
                (1 + d_ai + d_bj for d_bj in distances_b),
                (1 + d_bi + d_aj for d_aj in distances_a),
            )
        )


def get_total(distances: Distances) -> int:
    return sum(sum(line) for line in distances)


def prepare_distances(portals: int, links: list[Link], reach: int = 3) -> tuple[Distances, int]:
    distances = [[portals] * portals for _ in range(portals)]
    for a in range(portals):
        distances[a][a] = 0
        for b in range(a + 1, a + 1 + reach):
            distances[a][b % portals] = 1
            distances[b % portals][a] = 1
    reduce_distances(distances)
    initial_strain = get_total(distances)

    for link in links:
        add_link(distances, link)

    return distances, initial_strain


def part1(data: Data, reach: int = 1) -> int:
    portals, links = data

    distances, initial_strain = prepare_distances(portals, links, reach)
    final_strain = get_total(distances)

    return initial_strain - final_strain


def part2(data: Data, reach: int = 3) -> int:
    portals, links = data

    distances, initial_strain = prepare_distances(portals, links, reach)

    best = min(
        get_total(copy_with_link(distances, (a, b)))
        for a in range(portals)
        for b in range(a)
        if a - b > reach and portals - (a - b) > reach
    )

    return initial_strain - best


def copy_with_link(distances: Distances, link: Link) -> Distances:
    distances = distances[:]  # add_link creates new rows
    add_link(distances, link)
    return distances


def search(nodes: list[int], distances: Distances) -> int:
    if not nodes:
        return get_total(distances)

    return min(
        search(nodes[1:i] + nodes[i + 1 :], copy_with_link(distances, (nodes[0], nodes[i])))
        for i in range(1, len(nodes))
    )


def part3(data: Data, reach: int = 3) -> int:
    portals, links = data

    distances, initial_strain = prepare_distances(portals, links, reach)

    spread = portals // 8
    best = min(search([a + spread * i for i in range(8)], distances) for a in range(spread))

    return initial_strain - best
