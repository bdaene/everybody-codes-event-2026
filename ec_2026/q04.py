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
        result = {name: int(value) for name, value in (entry.split("=") for entry in line.strip().split())}
        results.append(Result(**result))

    return results


def compute_order_1(results: Data) -> list[int]:
    times = {}
    for result in results:
        times[result.id] = times.get(result.id, 0) + result.time

    return sorted(times.values())


def compute_order_2(results: Data) -> list[int]:
    times, parts = {}, {}
    for result in results:
        times[result.id] = times.get(result.id, 0) + result.time
        parts[result.id] = parts.get(result.id, 0) + 1

    order = sorted(times.keys(), key=lambda x: (-parts[x], times[x]))

    return [times[x] for x in order]


def compute_order_3(results: Data) -> list[int]:
    quests = {}
    for result in results:
        quest = quests.setdefault(result.quest, {})
        part = quest.setdefault(result.part, {})
        part[result.id] = result.time

    scores = {}
    for quest in quests.values():
        times = {}
        for part in sorted(quest):
            current_times = {}
            for id, time in quest[part].items():
                times[id] = times.get(id, 0) + time
                current_times.setdefault(times[id], set()).add(id)

            position = 0
            for time in sorted(current_times):
                for id in current_times[time]:
                    scores[id] = scores.get(id, 0) + max(part * 50 - position, 0)
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
