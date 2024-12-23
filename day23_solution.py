from aoc_tools.solution import Solution
import networkx as nx


class D23S(Solution):

    def __init__(self):
        super().__init__()
        self.day = 23
        self.expected_test_result_part_1 = 7
        self.expected_test_result_part_2 = "co,de,ka,ta"
        self.network = None

    def solve_part_1(self):
        self.get_graph()
        net_of_three = [clique for clique in nx.enumerate_all_cliques(self.network) if len(clique) == 3]
        count = 0
        for clique in net_of_three:
            for node in clique:
                if node.startswith("t"):
                    count += 1
                    break
        return count

    def solve_part_2(self):
        self.get_graph()
        party_net_list = list(reversed([clique for clique in nx.enumerate_all_cliques(self.network)]))
        party_net = party_net_list[0]
        party_net.sort()
        return ",".join(party_net)

    def get_graph(self):
        self.network = nx.Graph()
        for line in self.puzzle:
            parts = line.split("-")
            self.network.add_edge(parts[0], parts[1])

if __name__ == "__main__":
    D23S().test()
    D23S().solve()
