from functools import cache
from aoc_tools.solution import Solution
from aoc_tools.nfa import NFA, State

class D19aS(Solution):

    def __init__(self):
        super().__init__()
        self.day = 19
        self.expected_test_result_part_1 = 6
        self.expected_test_result_part_2 = 16
        self.tokens = None
        self.words = None

    def solve_part_1(self):
        self.get_tokens_and_words()
        nfa = NFA()
        for token in self.tokens:
            nfa.add_pattern(token)
        accepted = [word for word in self.words if nfa.accepts(word)]
        print(accepted)
        result = len(accepted)
        return result

    def solve_part_2(self):
        self.get_tokens_and_words()
        nfa = NFA()
        for token in self.tokens:
            nfa.add_pattern(token)
        count = sum([nfa.accepts(word) for word in self.words])
        print(count)
        return count

    def get_tokens_and_words(self):
        self.tokens = []
        self.words = []
        is_second_segment = False
        for line in self.puzzle:
            if line == "": is_second_segment = True
            elif is_second_segment: self.words.append(line)
            else: self.tokens += list(map(str.strip, line.split(",")))






if __name__ == "__main__":
    D19aS().test()
    D19aS().solve()
