import argparse
from pathlib import Path
from time import perf_counter_ns

from ec_2026 import PARTS, get_solver, input_path, load_quest


def run(quest: int, part: int, path: Path) -> None:
    parser, solver = get_solver(load_quest(quest), part)

    start = perf_counter_ns()
    data = parser(path.read_text())
    print(f"Parsing time: {(perf_counter_ns() - start) / 10**6:.3f} ms")

    start = perf_counter_ns()
    result = solver(data)
    print(f"Solving time: {(perf_counter_ns() - start) / 10**6:.3f} ms")
    print(f"Result: {result}")


def main() -> None:
    arg_parser = argparse.ArgumentParser(description="Run an Everybody Codes 2026 quest.")
    arg_parser.add_argument("quest", type=int)
    arg_parser.add_argument("part", type=int, nargs="?", choices=PARTS, help="default: all parts with an input file")
    arg_parser.add_argument(
        "-i", "--input", type=Path, help="input file (default: data/everybody_codes_e2026_qNN_pP.txt)"
    )
    args = arg_parser.parse_args()

    if args.input and args.part is None:
        arg_parser.error("--input requires a part")

    parts = [args.part] if args.part else [part for part in PARTS if input_path(args.quest, part).exists()]
    if not parts:
        arg_parser.error(f"no input file found for quest {args.quest} in data/")

    for part in parts:
        print(f"--- Quest {args.quest} part {part}")
        run(args.quest, part, args.input or input_path(args.quest, part))


if __name__ == "__main__":
    main()
