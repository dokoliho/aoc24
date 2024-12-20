from aoc_tools.animation_game import AnimationGame, Particle
from aoc_tools.animation_game import get_square, get_circle, ORANGE, GREEN
from day20_solution import D20S

class GameD20S(D20S):
    def animate_part_1(self, show_callback):
        ani = AnimationGame.instance
        self.get_walls_start_end()
        orange_block = get_square(ani.square_size-2, ORANGE)
        green_circle = get_circle((ani.square_size-2)//2, GREEN)
        for wall in self.walls:
            particle = Particle(wall[0] * ani.square_size , wall[1] * ani.square_size)
            particle.set_surface(orange_block)
            ani.particles.append(particle)
        self.find_path()
        self.get_pathmap()
        cheats = set()
        run = True
        while run:
            run = show_callback()

    def animate_part_2(self, show_callback):
        ani = AnimationGame.instance
        self.get_walls_start_end()
        orange_block = get_square(ani.square_size-2, ORANGE)
        green_circle = get_circle((ani.square_size-2)//2, GREEN)
        for wall in self.walls:
            particle = Particle(wall[0] * ani.square_size , wall[1] * ani.square_size)
            particle.set_surface(orange_block)
            ani.particles.append(particle)
        self.find_path()
        self.get_pathmap()
        cheats = set()
        run = True
        start_index = 0
        max_man_distance = 20
        pos_particle = []
        while run:
            if start_index < len(self.path):
                for particle in pos_particle: particle.is_alive = False
                indices = self.reachable_positions(self.path[start_index], max_man_distance)
                indices = filter(lambda x: x > start_index, indices)
                positions = [self.path[i] for i in indices]
                pos_particle = [Particle(pos[0]* ani.square_size, pos[1]* ani.square_size) for pos in positions]
                for particle in pos_particle: particle.set_surface(green_circle)
                ani.particles.extend(pos_particle)
                start_index += 1
            run = show_callback()

class AnimationGameD20S(AnimationGame):
    def win_height(self):
        if not self._solution.walls:
            self._solution.get_walls_start_end()
        return max([wall[1] for wall in self._solution.walls])

    def win_width(self):
        if not self._solution.walls:
            self._solution.get_walls_start_end()
        return max([wall[0] for wall in self._solution.walls])



if __name__ == "__main__":
    solution = GameD20S()
    animation = AnimationGameD20S(solution, "Race Condition", square_size=6, fps=25)
    animation.set_part(2)
    animation.set_test_input(False)
    animation.run()
