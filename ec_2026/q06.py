from collections import Counter, defaultdict

Data = dict[str, list[str]]


def parse(text: str) -> Data:
    notes = {}
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        key, values = line.split(":", 1)
        notes[key] = values.split(",")
    return notes


def explore(notes: Data, start: str = "NULL") -> set[str]:
    seen = {start}
    to_visit = [start]
    while to_visit:
        product = to_visit.pop()
        for ingredient in notes.get(product, []):
            if ingredient not in seen:
                seen.add(ingredient)
                to_visit.append(ingredient)

    return seen


def reverse(notes: Data) -> Data:
    reversed_notes = defaultdict(list)
    for product, ingredients in notes.items():
        for ingredient in ingredients:
            reversed_notes[ingredient].append(product)
    return reversed_notes


def part1(data: Data) -> int:
    ingredients = explore(data, start="NULL")
    return len(ingredients) - 1  # exclude "NULL"


def part2(data: Data) -> int:
    reversed_notes = reverse(data)
    products = explore(reversed_notes, start="NULL")
    return len(products) - 1


def part3(data: Data) -> int:
    reversed_notes = reverse(data)
    starts = {ingredient for ingredient in reversed_notes if ingredient.startswith("NULL")}
    products = Counter(product for start in starts for product in explore(reversed_notes, start=start))
    return sum(count >= 2 for product, count in products.items() if product not in starts)
