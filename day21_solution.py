from itertools import pairwise

from aoc_tools.solution import Solution
import networkx as nx

class D21S(Solution):

    def __init__(self):
        super().__init__()
        self.day = 21
        self.expected_test_result_part_1 = 126384
        self.expected_test_result_part_2 = 2
        self.numeric_keyboard = None
        self.directional_keyboard = None


    def solve_part_1(self):
        self.generate_keyboards()
        sum = 0
        for line in self.puzzle:
            radiation_sequences = self.all_shortest_paths(line, self.numeric_keyboard)
            freezing_sequences = []
            for s in radiation_sequences:
                freezing_sequences.extend(self.all_shortest_paths(s, self.directional_keyboard))
            historian_sequences = []
            for s in freezing_sequences:
                historian_sequences.extend(self.all_shortest_paths(s, self.directional_keyboard))
            historian_len = len(historian_sequences[0])-2
            num_part = int(line[:-1])
            print(f"Line: {line}, len: {historian_len}, num: {num_part}")
            sum += historian_len * num_part
        return sum

    def solve_part_2(self):
        return 2

    def generate_keyboards(self):
        numeric_edges = [
            ('7', '8', {'symbol': '>'}),
            ('8', '9', {'symbol': '>'}),
            ('4', '5', {'symbol': '>'}),
            ('5', '6', {'symbol': '>'}),
            ('1', '2', {'symbol': '>'}),
            ('2', '3', {'symbol': '>'}),
            ('0', 'A', {'symbol': '>'}),

            ('8', '7', {'symbol': '<'}),
            ('9', '8', {'symbol': '<'}),
            ('5', '4', {'symbol': '<'}),
            ('6', '5', {'symbol': '<'}),
            ('2', '1', {'symbol': '<'}),
            ('3', '2', {'symbol': '<'}),
            ('A', '0', {'symbol': '<'}),

            ('7', '4', {'symbol': 'v'}),
            ('8', '5', {'symbol': 'v'}),
            ('9', '6', {'symbol': 'v'}),
            ('4', '1', {'symbol': 'v'}),
            ('5', '2', {'symbol': 'v'}),
            ('6', '3', {'symbol': 'v'}),
            ('2', '0', {'symbol': 'v'}),
            ('3', 'A', {'symbol': 'v'}),

            ('4', '7', {'symbol': '^'}),
            ('5', '8', {'symbol': '^'}),
            ('6', '9', {'symbol': '^'}),
            ('1', '4', {'symbol': '^'}),
            ('2', '5', {'symbol': '^'}),
            ('3', '6', {'symbol': '^'}),
            ('0', '2', {'symbol': '^'}),
            ('A', '3', {'symbol': '^'}),
        ]
        self.numeric_keyboard = nx.DiGraph()
        self.numeric_keyboard.add_edges_from(numeric_edges)

        directional_edges = [
            ('^', 'A', {'symbol': '>'}),
            ('<', 'v', {'symbol': '>'}),
            ('v', '>', {'symbol': '>'}),

            ('A', '^', {'symbol': '<'}),
            ('>', 'v', {'symbol': '<'}),
            ('v', '<', {'symbol': '<'}),

            ('^', 'v', {'symbol': 'v'}),
            ('A', '>', {'symbol': 'v'}),

            ('v', '^', {'symbol': '^'}),
            ('>', 'A', {'symbol': '^'}),
            ]
        self.directional_keyboard = nx.DiGraph()
        self.directional_keyboard.add_edges_from(directional_edges)

    def all_shortest_numeric_paths(self, number_string):
        return self.all_shortest_paths(number_string, self.numeric_keyboard)

    def all_shortest_paths(self, string, keyboard):
        prefixes = [""]
        for start, end in pairwise('A'+string):
            new_prefixes = []
            for path in nx.all_shortest_paths(keyboard, start, end):
                edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
                symbols = [keyboard.get_edge_data(*edge)['symbol'] for edge in edges]
                for prefix in prefixes:
                    new_prefixes.append(prefix + "".join(symbols)+'A')
            prefixes = new_prefixes
        return prefixes

if __name__ == "__main__":
    D21S().test()
    D21S().solve()
