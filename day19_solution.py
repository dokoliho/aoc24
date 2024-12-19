from functools import cache
from aoc_tools.solution import Solution


class D19S(Solution):

    def __init__(self):
        super().__init__()
        self.day = 19
        self.expected_test_result_part_1 = 6
        self.expected_test_result_part_2 = 16
        self.tokens = None
        self.words = None

    def solve_part_1(self):
        self.get_tokens_and_words()
        result = len([word for word in self.words if self.is_word_in_language(word)])
        print(self.is_word_in_language.cache_info())
        self.is_word_in_language.cache_clear()
        return result

    def solve_part_2(self):
        self.get_tokens_and_words()
        result = sum([self.count_ways(word) for word in self.words])
        print(self.count_ways.cache_info())
        self.count_ways.cache_clear()
        return result

    def get_tokens_and_words(self):
        self.tokens = []
        self.words = []
        is_second_segment = False
        for line in self.puzzle:
            if line == "": is_second_segment = True
            elif is_second_segment: self.words.append(line)
            else: self.tokens += list(map(str.strip, line.split(",")))

    @cache
    def is_word_in_language(self, word):
        if len(word) == 0: return True
        for token in self.tokens:
            if word.startswith(token) and self.is_word_in_language(word[len(token):]): return True
        return False

    @cache
    def count_ways(self, word):
        if len(word) == 0: return 1
        return sum([self.count_ways(word[len(token):]) for token in self.tokens if word.startswith(token)])



if __name__ == "__main__":
    D19S().test()
    D19S().solve()
