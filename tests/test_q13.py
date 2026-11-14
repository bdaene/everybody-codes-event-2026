import pytest

from ec_2026 import solve

QUEST = 13

EXAMPLES = [
    # (part, example input, expected answer)
    (
        1,
        """\
hands 6:8:12
direction CW:CCW:CW
current 2:4:8
move 9:7:4
""",
        5,
    ),
    (
        1,
        """\
hands 6:8:12
direction CW:CCW:CW
current 1:2:2
move 10:12:15
""",
        7,
    ),
    (
        1,
        """\
hands 6:8:12
direction CW:CCW:CW
current 1:2:2
move 10:12:20
""",
        9,
    ),
    (
        2,
        """\
hands 6:8:12
direction CW:CCW:CW
current 2:4:8
move 9:7:4

hands 6:8:12
direction CW:CCW:CW
current 1:2:2
move 10:12:15

hands 6:8:12
direction CW:CCW:CW
current 1:2:2
move 10:12:20
""",
        21,
    ),
]


@pytest.mark.parametrize(("part", "text", "expected"), EXAMPLES)
def test_example(part: int, text: str, expected: int) -> None:
    assert solve(QUEST, part, text) == expected
