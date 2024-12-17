import curses

from day16_solution import D16S
from aoc_tools.animation import Animation
import time


class Animated_D16S(D16S):

    def get_walls_start_end(self):
        super().get_walls_start_end()
        ani = Animation.instance
        for row in range(len(self.puzzle)):
            for col in range(len(self.puzzle[0])):
                pos = (col, row)
                if pos in self.walls:
                    ani.output(col, row, "#", 8)
                elif pos == self.start:
                    ani.output_reverse(col, row, "S", 14)
                elif pos == self.end:
                    ani.output_reverse(col, row, "E", 14)
                else:
                    ani.output(col, row, " ", 8)
            ani.win.refresh()


    def mark_visited(self, node, visited, visited_cost, dist, pred):
        visited, visited_cost = super().mark_visited(node, visited, visited_cost, dist, pred)
        ani = Animation.instance
        pos, direction = node
        if pos != self.start:
            col, row = pos
            ani.output(col, row, "O", 4)
            ani.win.refresh()
            time.sleep(0.001)
        return visited, visited_cost

    def get_tiles_from_node(self, node, visited, tiles):
        ani = Animation.instance
        if node and node in visited:
            pos, _ = node
            if pos not in tiles:
                tiles.add(pos)
                col, row = pos
                ani.output(col, row, "X", 14)
                ani.win.refresh()
                time.sleep(0.001)
            for _, pred in visited[node]:
                tiles = self.get_tiles_from_node(pred, visited, tiles)
        return tiles



class D15S_Animation(Animation):
    pass

if __name__ == "__main__":
    animation = D15S_Animation(Animated_D16S())
    animation.set_part(2)
    animation.set_test_input(False)
    animation.run()