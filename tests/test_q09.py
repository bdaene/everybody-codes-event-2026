import pytest

from ec_2026 import solve

QUEST = 9

EXAMPLES = [
    # (part, example input, expected answer)
    (
        1,
        """\
id=1, growth=3, limit=10
id=2, growth=5, limit=20
id=3, growth=7, limit=30
""",
        27,
    ),
    (
        2,
        """\
id=1, growth=3, limit=10
id=2, growth=5, limit=20
id=3, growth=7, limit=30
""",
        42,
    ),
    (
        3,
        """\
id=1, growth=3, limit=10
id=2, growth=5, limit=20
id=3, growth=7, limit=30
""",
        42,
    ),
]


@pytest.mark.parametrize(("part", "text", "expected"), EXAMPLES)
def test_example(part: int, text: str, expected: int) -> None:
    assert solve(QUEST, part, text) == expected
