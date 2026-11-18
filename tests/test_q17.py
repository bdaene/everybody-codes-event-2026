import pytest

from ec_2026 import solve

QUEST = 17

EXAMPLES = [
    # (part, example input, expected answer)
    (
        1,
        """\
####.######
#.#.##..#..
##.##.##..#
#.#.###.###
#.###.###.#
###.##.#.##
""",
        21,
    ),
    (
        2,
        """\
####.######
#.#.##..#..
##.##.##..#
#.#.###.###
#.###.###.#
###.##.#.##
""",
        94,
    ),
    (
        3,
        """\
####.######
#.#.##..#..
##.##.##..#
#.#.###.###
#.###.###.#
###.##.#.##
""",
        31,
    ),
]


@pytest.mark.parametrize(("part", "text", "expected"), EXAMPLES)
def test_example(part: int, text: str, expected: int) -> None:
    assert solve(QUEST, part, text) == expected
