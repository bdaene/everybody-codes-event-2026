from pathlib import Path
from time import perf_counter_ns

from ec_2026.q1 import solve


DATA_PATH = Path(__file__).parent / 'data.txt'

def main(part: int = 1):
    start = perf_counter_ns()
    data = solve.parse_data(DATA_PATH)
    print(f'Parsing time: {(perf_counter_ns() - start)/10**6:.3f} ms')

    start = perf_counter_ns()
    result = solve.run(data, part=part)
    print(f"Solving time: {(perf_counter_ns() - start)/10**6:.3f} ms")
    print(f'Result: {result}')



if __name__ == '__main__':
    main(part=3)
