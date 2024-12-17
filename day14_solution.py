import math
from functools import reduce
from operator import mul

from aoc_tools.solution import Solution
from collections import Counter, defaultdict


class D14S(Solution):

    def __init__(self):
        super().__init__()
        self.day = 14
        self.expected_test_result_part_1 = 12
        self.expected_test_result_part_2 = 0
        self.width = None
        self.height = None

    def solve_part_1(self):
        self.set_size()
        robots = self.get_robots()
        robots = [self.move_robot(robot, 100) for robot in robots]
        return reduce(mul, map(len, self.split_quadrants(robots)))

    def solve_part_2(self):
        self.set_size()
        robots = self.get_robots()
        # cycle = self.cycle_all(robots)
        # the size of the grid are prime numbers, so the cycle is the product of the grid size
        cycle = self.width * self.height
        step = 0
        possible_solutions = []
        while step <= cycle:
            if self.is_possible_solution(robots):
                self.display(robots, step)
                possible_solutions.append(step)
            robots = [self.move_robot(robot, 1) for robot in robots]
            step += 1
        return possible_solutions[0] if len(possible_solutions) > 0 else 0

    def set_size(self):
        self.width, self.height = (11,7) if self.is_test else (101,103)

    def get_robots(self):
        robots = []
        for line in self.puzzle:
            robots.append(tuple([self.get_values(part) for part in line.split(" ")]))
        return robots

    def move_robot(self, robot, seconds):
        pos, vel = robot
        new_pos = ((pos[0] + vel[0] * seconds) % self.width,
                   (pos[1] + vel[1] * seconds) % self.height)
        return (new_pos, vel)

    def get_values(self, part):
        return tuple(map(int, part.split("=")[1].split(",")))


    def split_quadrants(self, robots):
        mid_w, mid_h = self.width // 2, self.height // 2
        quadrants = [
            (0, 0, mid_w - 1, mid_h - 1),
            (mid_w + 1, 0, self.width - 1, mid_h - 1),
            (0, mid_h + 1, mid_w - 1, self.height - 1),
            (mid_w + 1, mid_h + 1, self.width - 1, self.height - 1),
        ]
        return tuple(self.robots_in_area(robots, q) for q in quadrants)

    def robots_in_area(self ,robots, rect):
        x1, y1, x2, y2 = rect
        positions = [(robot[0][0]+self.width % self.width,
                        robot[0][1]+self.height % self.height)
                     for robot in robots]
        return [p for p in positions if x1 <= p[0] <= x2 and y1 <= p[1] <= y2]

    def cycle(self, robot):
        dx, dy = robot[1]
        dx = dx if dx > 0 else -dx
        dy = dy if dy > 0 else -dy
        vx = self.lcm(self.width, dx)
        vy = self.lcm(self.height, dy)
        return self.lcm(vx // dx, vy // dy)

    def cycle_all(self, robots):
        cycles = [self.cycle(robot) for robot in robots]
        return reduce(self.lcm, cycles)

    def lcm(self, a, b):
        return abs(a * b) // math.gcd(a, b)

    def is_possible_solution(self, robots):
        # My solution
        # A Xmax tree consists of at least a single line with more then 10 robots
        robot_rows = defaultdict(list)
        for pos, _ in robots:
            row = pos[1] % self.height
            col = pos[0] % self.width
            robot_rows[row].append(col)
        max_segments = [self.max_segment(sorted(col_list)) for col_list in robot_rows.values()]
        return max(max_segments) > 10

        # Reddit solution
        #counter = Counter([robot[0] for robot in robots])
        #return len(counter) == len(robots)


    def max_segment(self, sorted_cols):
        if len(sorted_cols) == 0:  # Leere Liste prüfen
            return 0
        longest = 0
        current = 1
        for i in range(1, len(sorted_cols)):
            longest = max(longest, current)
            if sorted_cols[i] == sorted_cols[i - 1] + 1:  # Folge ist zusammenhängend
                current += 1
            else:
                current = 1
        return longest

    def display(self, robots, step):
        print(f"Step {step}")
        counter = Counter([robot[0] for robot in robots])
        self.print_panel(counter)
        print()

    def print_panel(self, counter):
        panel = [["." for _ in range(self.width)] for _ in range(self.height)]
        for pos in counter:
            panel[pos[1]][pos[0]] = str(counter[pos])
        for row in panel:
            print("".join(row))

if __name__ == "__main__":
    D14S().test()
    D14S().solve()
