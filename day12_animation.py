from day12_solution import D12S
from aoc_tools.animation import Animation


class Animated_D12S(D12S):

    def merge_regions(self, garden_map):
        ani = Animation.instance
        for x in range(len(self.puzzle[0])):
            for y in range(len(self.puzzle)):
                pos = (x, y)
                union_count = self.merge_pos_with_neighbours(pos, garden_map)
                region = garden_map[pos].region
                if region not in ani.color_map: # Assign a color to the region
                    ani.color_map[region] = ani.next_color()
                if union_count > 1: # If the plant was merged with more than one neighbour, redraw the whole region
                    for (cx, cy), plant in garden_map.items():
                        if garden_map[(cx, cy)].region == region:
                            ani.output(cy, cx, plant.species, ani.color_map[region])
                            ani.win.refresh()
                else:
                    ani.output(y, x, garden_map[pos].species, ani.color_map[region])
                    ani.win.refresh()


class D12S_Animation(Animation):
    def __init__(self, solution):
        super().__init__(solution)
        self.color_map = {} # region -> color


if __name__ == "__main__":
    animation = D12S_Animation(Animated_D12S())
    animation.set_part(1)
    animation.set_test_input(False)
    animation.run()