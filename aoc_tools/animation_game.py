import pygame
from aoc_tools.solution import  Solution

BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (144, 238, 144)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
BROWN = (165, 42, 42)
PINK = (255, 192, 203)

def get_square(size, color):
    surface = pygame.Surface((size, size))
    surface.fill(color)
    return surface

def get_circle(radius, color):
    surface = pygame.Surface((2*radius, 2*radius), pygame.SRCALPHA)
    pygame.draw.circle(surface, color, (radius, radius), radius)
    return surface

class Particle:
    def __init__(self, x, y):
        self.position = (x, y)
        self._surface = None
        self.is_alive = True

    def set_surface(self, surface):
        self._surface = surface

    def draw(self, screen):
        if self._surface is not None:
            screen.blit(self._surface, self.position)

class AnimationGameSolution(Solution):
    def animate_part_1(self, show_callback):
        run = True
        while run:
            run = show_callback()

    def animate_part_2(self, show_callback):
        run = True
        while run:
            run = show_callback()


class AnimationGame:

    instance = None

    def __init__(self, solution, title, fps=5, square_size=10):
        AnimationGame.instance = self
        self._solution = solution
        self.title = title
        self.fps = fps
        self.size = None
        self.clock = pygame.time.Clock()
        self.screen = None
        self._rows = 0
        self._cols = 0
        self._test_input = False
        self._part = 0
        self.square_size = square_size
        self.particles = []

    def set_test_input(self, value):
        self._test_input = value

    def set_part(self, value):
        self._part = value

    def init_game(self, width, height):
        self.size = ((width+1) * self.square_size, (height+1) * self.square_size)
        pygame.init()
        pygame.display.set_caption(self.title)
        self.screen = pygame.display.set_mode(self.size)

    def show(self):
        if not self.event_handling(): return False
        if not self.update_game(): return False
        self.draw_game()
        self.clock.tick(self.fps)
        return True

    def exit_game(self):
        pygame.quit()

    def event_handling(self):  # bleibt in der Unterklasse unverändert
        for event in pygame.event.get():
            if not self.handle_event(event):
                return False
        return True

    def handle_event(self, event):  # wird in der Unterklasse überschrieben
        if event.type == pygame.QUIT:
            return False
        return True

    def update_game(self):
        self.particles = [particle for particle in self.particles if particle.is_alive]
        return True

    def draw_game(self):
        self.screen.fill(BLACK)
        for particle in self.particles:
            particle.draw(self.screen)
        pygame.display.flip()

    def run(self):
        if self._test_input:
            self._solution.read_test_input()
        else:
            self._solution.read_real_input()
        width = self.win_width()
        height = self.win_height()
        self.init_game(width, height)
        if (self._part & 0b0001) > 0: self._solution.animate_part_1(self.show)
        if (self._part & 0b0010) > 0: self._solution.animate_part_2(self.show)
        self.exit_game()

    def win_height(self):
        if self._solution.puzzle:
            return len(self._solution.puzzle)
        return 80

    def win_width(self):
        if self._solution.puzzle:
            return len(self._solution.puzzle[0])
        return 80


if __name__ == "__main__":
    solution = AnimationGameSolution()
    animation = AnimationGame(solution, "Animation Game")
    animation.set_part(2)
    animation.set_test_input(False)
    animation.run()