from day14_solution import D14S
from aoc_tools.animation import Animation
from collections import Counter
import time

class Animated_D14S(D14S):

    def display(self, robots, step):
        ani = Animation.instance
        counter = Counter([robot[0] for robot in robots])
        for x in range(self.width):
            for y in range(self.height):
                if (x, y) in counter:
                    ani.output(x, y, str(counter[(x, y)]), 2)
                else:
                    ani.output(x, y, " ", 2)
        ani.output(0, self.height, f"Step {step}")
        ani.win.refresh()
        time.sleep(1)


class D14S_Animation(Animation):

    def win_height(self):
        return 104

    def win_width(self):
        return 101


if __name__ == "__main__":
    animation = D14S_Animation(Animated_D14S())
    animation.set_part(2)
    animation.set_test_input(False)
    animation.run()