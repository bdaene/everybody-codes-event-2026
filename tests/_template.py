"""Copy to tests/test_qNN.py and set QUEST."""

import pytest

from ec_2026 import solve

QUEST = 0

EXAMPLES = [
    # (part, example input, expected answer)
    # (1, """\
    # paste example here
    # """, 0),
]


@pytest.mark.parametrize(("part", "text", "expected"), EXAMPLES)
def test_example(part: int, text: str, expected: int) -> None:
    assert solve(QUEST, part, text) == expected
