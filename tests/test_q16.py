import pytest

from ec_2026 import solve

QUEST = 16

EXAMPLES = [
    # (part, example input, expected answer)
    (
        1,
        """\
    RRGGBBGRRGGBBG
    """,
        3,
        {},
    ),
    (
        1,
        """\
    BBRGGRRGBBRGGBRGBBRRBRRRBGGRRRBGBGGBBRGGRRGBBRGGBRGBBRRBRRRBGGRRRBGBGG
    """,
        26,
        {},
    ),
    (
        1,
        """\
BBRGRBGGRBGRBBGRBGBG
""",
        8,
        {},
    ),
    (
        2,
        """\
BBRGRBGGRBGRBBGRBGBG
""",
        73,
        {"factor": 1},
    ),
    (
        2,
        """\
RRYGYBYG
""",
        1053,
        {},
    ),
    (
        3,
        """\
RRYGGYBBYG
""",
        135154,
        {},
    ),
]


@pytest.mark.parametrize(("part", "text", "expected", "kwargs"), EXAMPLES)
def test_example(part: int, text: str, expected: int, kwargs: dict) -> None:
    assert solve(QUEST, part, text, **kwargs) == expected
