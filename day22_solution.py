from collections import deque

from aoc_tools.solution import Solution

def mix(a, b):
    return a ^ b

def prune(a):
    return a % 0x1000000 # 16777216 - only the last 24 bits

def create_random_generator(start):
    num = start
    for _ in range(2000):
        # Step 1
        result = num << 6
        num = mix(num, result)
        num = prune(num)
        # Step 2
        result = num >> 5
        num = mix(num, result)
        num = prune(num)
        # Step 3
        result = num << 11
        num = mix(num, result)
        num = prune(num)
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

def create_price_map(start):
    m = {}
    for seq, price in create_sequence_generator(start):
        if seq not in m:
            m[seq] = price
    return m


class D22S(Solution):

    def __init__(self):
        super().__init__()
        self.day = 22
        self.expected_test_result_part_1 = 37327623
        self.expected_test_result_part_2 = 24

    def solve_part_1(self):
        result = 0
        for start in map(int, self.puzzle):
            gen = create_random_generator(start)
            for _ in range(1999): next(gen)
            result += next(gen)
        return result

    def solve_part_2(self):
        price_maps = []
        for start in map(int, self.puzzle):
            price_maps.append(create_price_map(start))
        all_sequences = set.union(*[set(price_map.keys()) for price_map in price_maps])
        bananas = []
        for sequence in all_sequences:
            result = 0
            for price_map in price_maps:
                result += price_map.get(sequence, 0)
            bananas.append((sequence, result))
        bananas.sort(reverse=True, key=lambda x: x[1])
        return bananas[0][1]




if __name__ == "__main__":
    D22S().test()
    D22S().solve()
