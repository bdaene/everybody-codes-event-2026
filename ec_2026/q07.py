from collections import Counter, defaultdict
from dataclasses import dataclass


@dataclass
class Cloud:
    id: int
    energy: int
    connections: list[int]


Data = list[Cloud]


def parse(text: str) -> Data:
    clouds = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        values = {
            key: list(map(int, value.split(","))) if key == "connections" else int(value)
            for key, value in (entry.split("=") for entry in line.split(", "))
        }
        clouds.append(Cloud(**values))

    return clouds


def propagate(clouds: Data, start_id: int, start_impulse: int = 5, limit: int | None = None) -> int:
    id_to_cloud = {cloud.id: cloud for cloud in clouds}
    n = max(id_to_cloud) + 1
    energies = [(id_to_cloud[cloud_id].energy if cloud_id in id_to_cloud else 0) for cloud_id in range(n)]
    exploded = [cloud_id not in id_to_cloud for cloud_id in range(n)]

    to_visit = {start_id: {start_impulse: 1}}
    while to_visit:
        to_visit_ = defaultdict(Counter)
        for cloud_id, impulses in to_visit.items():
            if exploded[cloud_id]:
                continue
            for impulse, paths in impulses.items():
                energies[cloud_id] += impulse * paths
                impulse -= 1
                if impulse < 1:
                    continue
                for connected_cloud in id_to_cloud[cloud_id].connections:
                    to_visit_[connected_cloud][impulse] += paths
        if limit is not None:
            for cloud_id, energy in enumerate(energies):
                if energy >= limit and not exploded[cloud_id]:
                    exploded[cloud_id] = True
                    for connected_cloud in id_to_cloud[cloud_id].connections:
                        to_visit_[connected_cloud][start_impulse] += 1
        to_visit = to_visit_

    return sum(energy for energy, exploded_cloud in zip(energies, exploded, strict=True) if not exploded_cloud)


def part1(clouds: Data, start_impulse: int = 5) -> int:
    start_id = max(clouds, key=lambda cloud: len(cloud.connections)).id
    return propagate(clouds, start_id, start_impulse)


def part2(clouds: Data) -> int:
    return part1(clouds, start_impulse=10)


def part3(clouds: Data, limit: int = 1_000_000) -> int:
    return max(propagate(clouds, cloud.id, start_impulse=10, limit=limit) for cloud in clouds)
