"""Quest 1 examples."""

import pytest

from ec_2026 import solve

QUEST = 1

EXAMPLES = [
    # (part, example input, expected answer)
    (1, "3,11,12,16,24,25", 11),
    (2, "3,11,12,16,24,25", 9),
    (3, "3,11,12,16,24,25", 61),
]


@pytest.mark.parametrize(("part", "text", "expected"), EXAMPLES)
def test_example(part: int, text: str, expected: int) -> None:
    assert solve(QUEST, part, text) == expected
