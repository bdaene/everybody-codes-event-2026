from dataclasses import dataclass
from itertools import combinations
from math import gcd
from typing import Literal

Direction = Literal[1, -1]
DIRECTIONS: dict[str, Direction] = {"CW": 1, "CCW": -1}


@dataclass
class Hand:
    positions: int
    direction: Direction
    current: int
    move: int


Portal = list[Hand]
Data = list[Portal]


def parse_portal(lines: list[str]) -> Portal:
    columns = [line.split(" ", 1)[-1].split(":") for line in lines]
    return [
        Hand(int(positions), DIRECTIONS[direction], int(current), int(move))
        for positions, direction, current, move in zip(*columns, strict=True)
    ]


def parse(text: str) -> Data:
    portals: Data = []
    lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            lines.append(stripped)
        elif lines:
            portals.append(parse_portal(lines))
            lines = []
    if lines:
        portals.append(parse_portal(lines))
    return portals


def count_zeros_in_window(offset: int, speed: int, period: int, move: int) -> int:
    ticks_before_0 = (period - offset) if speed > 0 else offset
    ticks = move * abs(speed)
    if ticks_before_0 > ticks:
        return 0
    return (ticks_before_0 > 0) + (ticks - ticks_before_0) // period


def count_meetings(hand_1: Hand, hand_2: Hand) -> int:
    if hand_1.move < hand_2.move:
        hand_1, hand_2 = hand_2, hand_1

    divisor = gcd(hand_1.positions, hand_2.positions)
    period = hand_1.positions * hand_2.positions // divisor
    speed_1, speed_2 = hand_2.positions // divisor, hand_1.positions // divisor

    # hand 2 move relative to hand 1
    offset = (hand_2.current * speed_2 - hand_1.current * speed_1) % period
    speed = speed_2 * hand_2.direction - speed_1 * hand_1.direction
    count = count_zeros_in_window(offset, speed, period, hand_2.move)

    # hand 2 stops
    offset = (offset + hand_2.move * speed) % period
    speed -= speed_2 * hand_2.direction
    count += count_zeros_in_window(offset, speed, period, hand_1.move - hand_2.move)

    return count


def part1(data: Data) -> int:
    return sum(count_meetings(hand_1, hand_2) for portal in data for hand_1, hand_2 in combinations(portal, 2))


# Every part uses the same portals, only their number and hands changes.
part3 = part2 = part1
