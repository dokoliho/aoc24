from solution import Solution


class D13S(Solution):

    class Challenge:
        def __init__(self, button_a, button_b, destination):
            self._button_a = button_a
            self._button_b = button_b
            self._destination = destination
            self.no_limit = False

        def solve(self):
            dx, dy = self._destination
            cost_a, ax, ay = self._button_a
            cost_b, bx, by = self._button_b
            det = ax * by - ay * bx
            if det == 0: return None # No unique solution exists (determinant is zero)
            num_a = dx * by - dy * bx
            num_b = dy * ax - dx * ay
            if num_a % det != 0 or num_b % det != 0: return None # No integer solution exists
            a = num_a // det
            b = num_b // det
            if (a > 100 or b > 100) and not self.no_limit: return None
            return a, b, a * cost_a + b * cost_b


    def __init__(self):
        super().__init__()
        self.day = 13
        self.expected_test_result_part_1 = 480
        self.expected_test_result_part_2 = 875318608908

    def solve_part_1(self):
        challenges = self.get_challenges()
        return self.get_cost_of_challenges(challenges)

    def solve_part_2(self):
        challenges = self.get_challenges(adjustment=10000000000000)
        return self.get_cost_of_challenges(challenges)

    def get_cost_of_challenges(self, challenges):
        # None als Filter-Funktion bedeutet, dass die Werte selbst das Filterkriterium sind
        # Wenn der Wert also None ist, wird er nicht in die Liste aufgenommen
        solutions = filter(None, map(lambda c: c.solve(), challenges))
        total = sum(cost for _, _, cost in solutions)
        return total

    def get_challenges(self, adjustment=0):
        challenges = []
        for i in range(0, len(self.puzzle), 4):
            button_a = self.get_button(self.puzzle[i], 3)
            button_b = self.get_button(self.puzzle[i+1], 1)
            destination = self.get_destination(self.puzzle[i+2], adjustment)
            challenge = self.Challenge(button_a, button_b, destination)
            challenge.no_limit = (adjustment > 0)
            challenges.append(challenge)
        return challenges

    def get_button(self, line, cost):
        dx, dy = tuple([int(v.split("+")[1]) for v in line.split(":")[1].strip().split(",")])
        return (cost, dx, dy)

    def get_destination(self, line, adjustment):
        return tuple([int(v.split("=")[1])+adjustment for v in line.split(":")[1].strip().split(",")])

if __name__ == "__main__":
    D13S().test()
    D13S().solve()
