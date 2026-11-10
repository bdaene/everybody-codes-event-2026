"""Copy to tests/test_qNN.py and set QUEST."""

import pytest

from ec_2026 import solve

QUEST = 11

EXAMPLES = [
    # (part, example input, expected answer)
    (
        1,
        """\
portals: 10

5 10
2 7
""",
        60,
    ),
    (
        2,
        """\
portals: 10

5 10
2 7
""",
        6,
    ),
    (
        3,
        """\
portals: 32

1 10
20 30
15 29
13 10
""",
        854,
    ),
    (
        3,
        """\
portals: 64

1 40
3 35
5 42
7 50
""",
        9634,
    ),
]


@pytest.mark.parametrize(("part", "text", "expected"), EXAMPLES)
def test_example(part: int, text: str, expected: int) -> None:
    assert solve(QUEST, part, text) == expected
