from solution import Solution
from itertools import product
import math


def add(a, b):
    return a + b

def mul(a, b):
    return a * b

def concat(a, b):
    if b == 0:
        return a * 10 + b  # Special case for single-digit 0
    b_length = int(math.log10(b)) + 1
    return a * (10 ** b_length) + b

OPERATIONS = [add, mul]
OPERATIONS2 = [add, mul, concat]

class Day07Solution(Solution):


    def __init__(self):
        super().__init__()
        self.day = 7
        self.expected_test_result_part_1 = 3749
        self.expected_test_result_part_2 = 11387
        self.equations = None

    def solve_part_1(self):
        self.get_equations()
        return sum([e[0] for e in self.equations if self.is_valid(e, OPERATIONS)])

    def get_equations(self):
        results, operands = zip(*[line.split(":") for line in self.puzzle])
        operands = [tuple(map(int, op_str.split())) for op_str in operands]
        results = list(map(int, results))
        self.equations = list(zip(results, operands))

    def is_valid(self, equation, possible_operations):
        count = len(equation[1]) - 1
        for operations in product(possible_operations, repeat=count):
            if self.is_valid_with_operations(equation, operations):
                return True
        return False

    def is_valid_with_operations(self, equation, operations):
        result, operands = equation
        return result == self.calculate_result(operands, operations, result)

    def calculate_result(self, operands, operations, limit=None):
        result = operands[0]
        for i, op in enumerate(operations):
            result = op(result, operands[i + 1])
            if limit and result > limit:
                return -1
        return result

    def solve_part_2(self):
        self.get_equations()
        return sum([e[0] for e in self.equations if self.is_valid(e, OPERATIONS2)])



if __name__ == "__main__":
    Day07Solution().test()
    Day07Solution().solve()
