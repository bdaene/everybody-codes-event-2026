from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Result:
    id: int
    quest: int
    part: int
    time: int


Data = list[Result]


def parse(text: str) -> Data:
    results = []
    for line in text.splitlines():
        if not line.strip():
            continue
        result = {name: int(value) for name, value in (entry.split("=") for entry in line.strip().split())}
        results.append(Result(**result))

    return results


def compute_order_1(results: Data) -> list[int]:
    times = defaultdict(int)
    for result in results:
        times[result.id] += result.time

    return sorted(times.values())


def compute_order_2(results: Data) -> list[int]:
    times, parts = defaultdict(int), defaultdict(int)
    for result in results:
        times[result.id] += result.time
        parts[result.id] += 1

    order = sorted(times.keys(), key=lambda x: (-parts[x], times[x]))

    return [times[x] for x in order]


def compute_order_3(results: Data) -> list[int]:
    quests = {}
    for result in results:
        quest = quests.setdefault(result.quest, {})
        part = quest.setdefault(result.part, {})
        part[result.id] = result.time

    scores = defaultdict(int)
    for quest in quests.values():
        times = defaultdict(int)
        for part in sorted(quest):
            current_times = defaultdict(list)
            for player, time in quest[part].items():
                times[player] += time
                current_times[times[player]].append(player)

            position = 0
            for time in sorted(current_times):
                for player in current_times[time]:
                    scores[player] += max(part * 50 - position, 0)
                position += len(current_times[time])

    return sorted(scores.values(), reverse=True)


def ranking_checksum(order: list[int]) -> int:
    position, prev, count, checksum = 0, None, 1, 0
    for result in order:
        if result == prev:
            count += 1
        else:
            position += count
            count = 1
            prev = result
        checksum += position * result

    return checksum


def part1(data: Data) -> int:
    return ranking_checksum(compute_order_1(data))


def part2(data: Data) -> int:
    return ranking_checksum(compute_order_2(data))


def part3(data: Data) -> int:
    return ranking_checksum(compute_order_3(data))
