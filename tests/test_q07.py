import pytest

from ec_2026 import solve

QUEST = 7

EXAMPLES = [
    # (part, example input, expected answer, solver kwargs)
    (
        1,
        """\
id=1, energy=5, connections=2,5,7
id=2, energy=9, connections=6,7
id=3, energy=3, connections=4
id=4, energy=8, connections=3
id=5, energy=1, connections=6,7
id=6, energy=7, connections=1,7
id=7, energy=6, connections=5
""",
        102,
        {},
    ),
    (
        2,
        """\
id=1, energy=5, connections=2,5,7
id=2, energy=9, connections=6,7
id=3, energy=3, connections=4
id=4, energy=8, connections=3
id=5, energy=1, connections=6,7
id=6, energy=7, connections=1,7
id=7, energy=6, connections=5
""",
        1316,
        {},
    ),
    (
        2,
        """\
id=1, energy=5, connections=2,3,5,7
id=2, energy=9, connections=1,3,4,5,6,7
id=3, energy=3, connections=1,2,4,6,7
id=4, energy=8, connections=1,2,7
id=5, energy=1, connections=2,3,4,6
id=6, energy=7, connections=1,2,3,4
id=7, energy=6, connections=1,2,4,6
""",
        1214633,
        {},
    ),
    (
        3,
        """\
id=1, energy=5, connections=2,5,7
id=2, energy=9, connections=6,7
id=3, energy=3, connections=4
id=4, energy=8, connections=3
id=5, energy=1, connections=6,7
id=6, energy=7, connections=1,7
id=7, energy=6, connections=5
""",
        187,
        {"limit": 100},
    ),
]


@pytest.mark.parametrize(("part", "text", "expected", "kwargs"), EXAMPLES)
def test_example(part: int, text: str, expected: int, kwargs: dict) -> None:
    assert solve(QUEST, part, text, **kwargs) == expected
