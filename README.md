# Everybody Codes 2026

Solutions for the [Everybody Codes 2026 event](https://everybody.codes/event/2026/quests).

## Setup

```sh
uv sync
uv run pre-commit install
```

## Inputs

Save puzzle inputs in `data/` with the download name, e.g. `data/everybody_codes_e2026_q04_p3.txt`.
They are personal and git-ignored.

## Run

```sh
uv run main.py 4        # all parts of quest 4 that have an input file
uv run main.py 4 3      # quest 4, part 3
uv run main.py 4 3 -i some_file.txt
```

## Adding a quest

Create `ec_2026/qNN.py` defining:

- `parse(text: str) -> Data`, plus an optional `parse_partN(text)` override when a part's input differs;
- `part1(data)`, `part2(data)`, `part3(data)`. Parts that share logic alias or call each other (`part2 = part1`, or a
  shared helper with different arguments).

Copy `tests/_template.py` to `tests/test_qNN.py`, set `QUEST`, and add the examples from the quest text.

## Checks

```sh
uv run pytest
uv run ruff check . && uv run ruff format .
uv run pre-commit run --all-files
```
