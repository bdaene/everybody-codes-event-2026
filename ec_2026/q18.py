from dataclasses import dataclass


@dataclass
class Stack:
    x: int
    y: int
    width: int = 1

    @property
    def right_x(self) -> int:
        return self.x + self.width - 1


Data = list[Stack]


def parse(text: str) -> Data:
    stacks = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        fields = {k: int(v) for k, v in (entry.split("=") for entry in line.split())}
        stacks.append(Stack(**fields))

    return stacks


def fill(stacks: list[Stack]) -> int:
    if not stacks:
        return 0

    stacks = sorted(stacks, key=lambda s: s.x)

    total = 0
    top = stacks[0]
    for stack in stacks:
        if stack.y <= top.y:
            continue
        total += top.y * (stack.x - top.x)
        top = stack
    top_left = top

    top = stacks[-1]
    for stack in reversed(stacks):
        if stack.y <= top.y:
            continue
        total += top.y * (top.right_x - stack.right_x)
        top = stack
    top_right = top

    total += (top_right.right_x - top_left.x + 1) * top_left.y

    return total


part3 = part2 = part1 = fill
