import pytest

from ec_2026 import solve

QUEST = 3

EXAMPLES = [
    # (part, example input, expected answer)
    (
        1,
        """\
    ISO-3210 7654
ISO-8742 2468
ISO-1111 1111
""",
        1478,
    ),
    (
        2,
        """\
ISO-3210 7654
ISO-8742 2468
ISO-1 1111
ISO-13 777
ISO-34 140856
ISO-789 2465112
ISO-2341 945
""",
        1161463,
    ),
    (
        3,
        """\
ISO2-3 23
ISO2-61 149
ISO2-978 99
ISO2-5887 5923
ISO2-76988 123749
ISO2-435657 929977
ISO2-3949 870737
""",
        50987,
    ),
]


@pytest.mark.parametrize(("part", "text", "expected"), EXAMPLES)
def test_example(part: int, text: str, expected: int) -> None:
    assert solve(QUEST, part, text) == expected
