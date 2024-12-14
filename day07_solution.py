from aoc_tools.solution import Solution
from operator import add, mul

def concat(a, b):
    return int(str(a)+str(b))

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
        return sum([e[0] for e in self.equations if self.is_valid_recursive(e, OPERATIONS)])

    def get_equations(self):
        results, operands = zip(*[line.split(":") for line in self.puzzle])
        operands = [tuple(map(int, op_str.split())) for op_str in operands]
        results = list(map(int, results))
        self.equations = list(zip(results, operands))

    def is_valid_recursive(self, equation, possible_operations):
        expected_result, operands = equation
        if len(operands) == 1:
            return expected_result == operands[0]
        for op in possible_operations:
            result = op(operands[0], operands[1])
            if result > expected_result:
                continue
            new_operands = (result,) + operands[2:]
            if self.is_valid_recursive((expected_result, new_operands), possible_operations):
                return True
        return False

    def solve_part_2(self):
        self.get_equations()
        return sum([e[0] for e in self.equations if self.is_valid_recursive(e, OPERATIONS2)])



if __name__ == "__main__":
    Day07Solution().test()
    Day07Solution().solve()
