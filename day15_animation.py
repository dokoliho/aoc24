import curses

from day15_solution import D15S
from aoc_tools.animation import Animation
import time


class Animated_D15S(D15S):

    def __init__(self):
        super().__init__()
        self.visualizations = True

    def display_map(self):
        ani = Animation.instance
        for row in range(self.height):
            for col in range(self.width):
                pos = (col,row)
                if pos == tuple(self.robot):
                    ani.output_bold(col, row, "@", 5)
                elif pos not in self.map:
                    ani.output(col, row, " ", 2)
                else:
                    char = self.map[pos]
                    if char == "#":
                        ani.output(col, row, "#", 2)
                    elif char in  "O[]":
                        ani.output_reverse(col, row, char , 3)
                    else:
                        ani.output(col, row, " ", 2)
        ani.win.refresh()



class D15S_Animation(Animation):

    def win_height(self):
        if self._solution.puzzle:
            return self._solution.puzzle.index("")
        return 0

    def win_width(self):
        return super().win_width() * self._part # Double on part 2

if __name__ == "__main__":
    animation = D15S_Animation(Animated_D15S())
    animation.set_part(2)
    animation.set_test_input(False)
    animation.run()