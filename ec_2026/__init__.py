"""Everybody Codes 2026 solutions.

Each quest module ``qNN`` defines:
  - ``parse(text: str) -> Data``: shared input parser,
  - ``parse_partN(text: str) -> Data`` (optional): parser override for part N,
  - ``part1(data)``, ``part2(data)``, ``part3(data)``: solvers.

Parts sharing logic simply alias or call each other (``part2 = part1``).
"""

from collections.abc import Callable
from importlib import import_module
from pathlib import Path
from types import ModuleType
from typing import Any

DATA_DIR = Path(__file__).parent.parent / "data"
PARTS = (1, 2, 3)


def load_quest(quest: int) -> ModuleType:
    return import_module(f"{__name__}.q{quest:02d}")


def input_path(quest: int, part: int) -> Path:
    return DATA_DIR / f"everybody_codes_e2026_q{quest:02d}_p{part}.txt"


def get_solver(module: ModuleType, part: int) -> tuple[Callable[[str], Any], Callable[[Any], Any]]:
    solver = getattr(module, f"part{part}", None)
    if solver is None:
        raise NotImplementedError(f"{module.__name__} has no part{part}")
    parser = getattr(module, f"parse_part{part}", None) or module.parse
    return parser, solver


def solve(quest: int, part: int, text: str) -> Any:
    parser, solver = get_solver(load_quest(quest), part)
    return solver(parser(text))
