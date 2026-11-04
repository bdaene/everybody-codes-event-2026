from dataclasses import dataclass
from pathlib import Path


@dataclass
class Result:
    id: int
    quest: int
    part: int
    time: int


Data = list[Result]


def parse_data(path: Path) -> Data:
    results = []
    for line in path.read_text().splitlines():
        result = {name: int(value) for name, value in (entry.split('=') for entry in line.strip().split())}
        results.append(Result(**result))

    return results


def compute_order_1(results: Data) -> list[int]:
    times = {}
    for result in results:
        times[result.id] = times.get(result.id, 0) + result.time

    return sorted(times.values())


def compute_order_2(results: Data) -> list[int]:
    times, parts, ids = {}, {}, set()
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


def run(data: Data, part: int = 0) -> int:
    if part == 1:
        order = compute_order_1(data)
    elif part == 2:
        order = compute_order_2(data)
    elif part == 3:
        order = compute_order_3(data)
    else:
        raise ValueError('Invalid part.')

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
