from aoc_tools.solution import Solution
from collections import deque, defaultdict

def mix_and_prune(a, b):
    return (a^b) % 0x1000000 # 16777216 - only the last 24 bits

def create_random_generator(start):
    num = start
    for _ in range(2000):
        # Step 1
        num = mix_and_prune(num, num << 6)
        # Step 2
        num = mix_and_prune(num, num >> 5)
        # Step 3
        num = mix_and_prune(num, num << 11)
        yield num

def create_price_generator(start):
    yield start % 10
    gen = create_random_generator(start)
    for value in gen:
        yield value % 10

def create_sequence_generator(start):
    gen = create_price_generator(start)
    seq = deque([])
    old_price = next(gen)
    for price in gen:
        seq.append(price - old_price)
        if len(seq) > 4: seq.popleft()
        if len(seq) == 4: yield tuple(seq), price
        old_price = price


class D22S(Solution):

    def __init__(self):
        super().__init__()
        self.day = 22
        self.expected_test_result_part_1 = 37327623
        self.expected_test_result_part_2 = 23

    def solve_part_1(self):
        result = 0
        for start in map(int, self.puzzle):
            gen = create_random_generator(start)
            for _ in range(1999):
                next(gen)
            result += next(gen)
        return result

    def solve_part_2(self):
        if self.is_test:
            self.puzzle = [
                "1",
                "2",
                "3",
                "2024",
            ]
        price_map = defaultdict(int)
        for start in map(int, self.puzzle):
            seen = set()
            for seq, price in create_sequence_generator(start):
                if seq not in seen:
                    seen.add(seq)
                    price_map[seq] += price
        return max(price_map.values())


if __name__ == "__main__":
    D22S().test()
    D22S().solve()
