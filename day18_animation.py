import curses

from day18_solution import D18S
from aoc_tools.animation import Animation
import time


class Animated_D18S(D18S):

    def solve_part_2(self):
        self.get_memory()
        ani = Animation.instance
        ani.wait_for_key()
        for self.steps in range(len(self.puzzle)):
            _ , path  = self.get_distance()
            self.display(path)
            if path is None:
                break
        return self.puzzle[self.steps]

    def display(self, path):
        ani = Animation.instance
        for row in range(self.height):
            for col in range(self.width):
                pos = (col,row)
                if pos in self.memory and self.memory[pos] < self.steps:
                    ani.output(col, row, "#", 2 if self.memory[pos] < self.steps-1 else 14)
                elif path and pos in path:
                    ani.output_reverse(col, row, "X", 3)
                elif path:
                    ani.output(col, row, " ", 2)
        ani.win.refresh()
        time.sleep(0.01)

class D18S_Animation(Animation):

    def win_height(self):
        return self._solution.height

    def win_width(self):
        return self._solution.width

if __name__ == "__main__":
    animation = D18S_Animation(Animated_D18S())
    animation.set_part(2)
    animation.set_test_input(False)
    animation.run()