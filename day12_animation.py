import time
from collections import defaultdict

from day12_solution import D12S, DIRECTIONS
import curses
import random

class Animation(D12S):

    colors = [curses.COLOR_BLACK,
              curses.COLOR_WHITE,
              curses.COLOR_GREEN,
              curses.COLOR_YELLOW,
              curses.COLOR_BLUE,
              curses.COLOR_MAGENTA,
              curses.COLOR_CYAN,
              curses.COLOR_RED]

    def __init__(self, rows, cols):
        super().__init__()
        self._rows = rows
        self._cols = cols
        self._win = None
        curses.start_color()
        self.color_count = 0
        for color in self.colors[1:]:
            self.color_count += 1
            curses.init_pair(self.color_count, color, curses.COLOR_BLACK)
        self.color_map = {}
        self._generator = self.next_color_generator()

    @property
    def win(self):
        return self._win

    def create_window(self, width, height):
        start_y, start_x = (self._rows - height - 2) // 2, (self._cols - width - 2) // 2
        with open("day12_log.txt", "w") as file:
            file.write(f"Screen: {self._cols}, {self._rows}\n")
            file.write(f"Window: {width}, {height}\n")
            file.write(f"Start: {start_x}, {start_y}\n")
        self._win = curses.newwin(height+2, width+2, start_y, start_x)
        curses.start_color()
        self._win.border()

    def output(self, x, y, text, color=6):
        self.win.addstr(y+1, x+1, text, curses.color_pair(color))

    def next_color_generator(self):
        count = 0
        while True:
            yield count+1
            count = (count + 1) % self.color_count

    def close_window(self):
        if self._win is not None:
            while True:
                key = self.win.getkey()
                if key == 'q': break
            return
            self._win.clear()
            self._win.refresh()
            self._win = None

    def solve_part_1(self):
        self.create_window(height=len(self.puzzle), width=len(self.puzzle[0]))
        garden_map = self.read_input()
        regions = self.find_regions(garden_map)
        result = sum([size*fences for size, fences, _ in regions.values()])
        self.close_window()
        return result



    def read_input(self):
        garden_map = {}
        for x in range(len(self.puzzle[0])):
            for y in range(len(self.puzzle)):
                garden_map[(x, y)] = D12S.Plant(self.puzzle[y][x])
        for x in range(len(self.puzzle[0])):
            for y in range(len(self.puzzle)):
                self.merge_with_neighbours(garden_map, x, y)
                region = garden_map[(x, y)].region
                if region not in self.color_map:
                    self.color_map[region] = next(self._generator)
                for (cx, cy), plant in garden_map.items():
                    if garden_map[(cx, cy)].region == region:
                        self.output(cy, cx, plant.species, self.color_map[region])
                        self.win.refresh()
                        time.sleep(0.001)

        return garden_map

def main(stdscr):
    stdscr.clear()
    rows, cols = stdscr.getmaxyx()
    Animation(rows, cols).solve()



if __name__ == "__main__":
    curses.wrapper(main)