from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from itertools import count

Data = list[str]
Grid = Data


def parse(text: str) -> Data:
    return [line.strip() for line in text.splitlines() if line.strip()]


@dataclass
class Ghost:
    row: int
    col: int
    direction: int
    life: int


DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def get_ghosts(grid: Grid, life: int) -> list[Ghost]:
    ghosts = []
    for row, line in enumerate(grid):
        for col, cell in enumerate(line):
            if cell in ".#":
                continue
            direction = ">v<^".index(cell)
            ghosts.append(Ghost(row, col, direction, life))

    return ghosts


def step(ghosts: Iterable[Ghost], grid: Grid):
    for ghost in ghosts:
        if ghost.life <= 0:
            continue
        dr, dc = DIRECTIONS[ghost.direction % len(DIRECTIONS)]
        if grid[ghost.row + dr][ghost.col + dc] == "#":
            ghost.life -= 1
            ghost.direction += 1
        else:
            ghost.row += dr
            ghost.col += dc


def check_overlap(ghosts: Iterable[Ghost]):
    positions = defaultdict(list[Ghost])
    for ghost in ghosts:
        if ghost.life <= 0:
            continue
        positions[(ghost.row, ghost.col)].append(ghost)

    for overlapped_ghosts in positions.values():
        if len(overlapped_ghosts) <= 1:
            continue
        for ghost in overlapped_ghosts:
            ghost.direction += 2
            ghost.life -= 1


def part1(data: Data, rounds: int = 10) -> int:
    grid = data
    ghosts = get_ghosts(grid, rounds)

    for _ in range(rounds):
        step(ghosts, grid)
        check_overlap(ghosts)

    return len(ghosts) * rounds - sum(ghost.life for ghost in ghosts)


def part2(data: Data, life: int = 10_000) -> int:
    grid = data
    ghosts = get_ghosts(grid, life)

    for round in count(1):
        step(ghosts, grid)
        check_overlap(ghosts)
        if not sum(ghost.life > 0 for ghost in ghosts):
            return round

    raise AssertionError


def get_state(ghosts: Iterable[Ghost]):
    return (
        tuple((ghost.row, ghost.col, ghost.direction % len(DIRECTIONS)) for ghost in ghosts if ghost.life > 0),
        tuple(ghost.life for ghost in ghosts),
    )


State = tuple[tuple[int, int, int], ...]


def part3(data: Data, life: int = 1_000_000_000_000) -> int:
    grid = data
    ghosts = get_ghosts(grid, life)

    seen_states: dict[State, tuple[int, tuple[int, ...]]] = {}

    round = 0
    while any(ghost.life > 0 for ghost in ghosts):
        state, lives = get_state(ghosts)

        if state in seen_states:
            prev_round, prev_lives = seen_states[state]
            cycles = min(
                (ghost.life - 1) // (prev_life - life)
                for ghost, life, prev_life in zip(ghosts, lives, prev_lives, strict=True)
                if ghost.life > 0
            )
            print(f"Match {prev_round} -> {round}. Skipping {round - prev_round}*{cycles} rounds")
            round += (round - prev_round) * cycles
            for ghost, life, prev_life in zip(ghosts, lives, prev_lives, strict=True):
                if ghost.life <= 0:
                    continue
                ghost.life -= (prev_life - life) * cycles
            seen_states.clear()
            state, lives = get_state(ghosts)

        seen_states[state] = (round, lives)

        round += 1
        step(ghosts, grid)
        check_overlap(ghosts)

    return round
