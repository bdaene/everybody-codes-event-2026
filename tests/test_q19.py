import pytest

from ec_2026 import solve

QUEST = 19

EXAMPLES = [
    # (part, example input, expected answer)
    (
        1,
        """\
CCCCC
MMMMM
YYYYY
KKKKK
CCMYY

CMYKC
CMYKC
CMYKC
CMYKC
CMYKC
""",
        144,
    ),
    (
        2,
        """\
CCCCC
MMMMM
YYYYY
KKKKK
CCMYY

14231
14231
14231
14231
14231
""",
        180,
    ),
    (
        3,
        """\
CCMM
YYKK
""",
        18,
    ),
    (
        3,
        """\
CCCMMM
CCMMYY
CCCYKK
CMMYYK
""",
        343,
    ),
    (
        3,
        """\
CCCCYMMM
CCMMMYYY
CCCYYYMM
MMCCCYYY
YYYMMMCC
CCYYMMKK
MMYYCCKK
YYYCCMMM
""",
        8000,
    ),
]


@pytest.mark.parametrize(("part", "text", "expected"), EXAMPLES)
def test_example(part: int, text: str, expected: int) -> None:
    assert solve(QUEST, part, text) == expected
