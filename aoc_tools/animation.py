import curses

class Animation:

    colors = [curses.COLOR_BLACK,
              curses.COLOR_WHITE,
              curses.COLOR_GREEN,
              curses.COLOR_YELLOW,
              curses.COLOR_BLUE,
              curses.COLOR_MAGENTA,
              curses.COLOR_CYAN,
              curses.COLOR_RED]

    instance = None

    def __init__(self, solution):
        Animation.instance = self
        self._solution = solution
        self._win = None
        self._stdscr = None
        self._rows = 0
        self._cols = 0
        self._test_input = False
        self._part = 0
        self.color_count = 0
        self._color_generator = self.next_color_generator()

    @property
    def win(self):
        return self._win

    def set_test_input(self, value):
        self._test_input = value

    def set_part(self, value):
        self._part = value

    def init_colors(self):
        curses.start_color()
        curses.use_default_colors()

        for color in self.colors:
            if color != curses.COLOR_BLACK:
                self.color_count += 1
                curses.init_pair(self.color_count, color, curses.COLOR_BLACK)
        for color in self.colors:
            if color != curses.COLOR_WHITE:
                self.color_count += 1
                curses.init_pair(self.color_count, color, curses.COLOR_WHITE)



    def next_color_generator(self):
        count = 0
        while True:
            yield count + 1
            count = (count + 1) % self.color_count

    def next_color(self):
        return next(self._color_generator)

    def create_window(self, width, height):
        start_y, start_x = (self._rows - height - 2) // 2, (self._cols - width - 2) // 2
        if start_y < 0:
            raise ValueError(f"Window height too large ({height}). Resize terminal.")
        if start_x < 0:
            raise ValueError(f"Window width too large ({width}). Resize terminal.")
        self._win = curses.newwin(height + 2, width + 2, start_y, start_x)
        self.init_colors()
        self._win.border()

    def output(self, x, y, text, color=0):
        self.win.addstr(y + 1, x + 1, text, curses.color_pair(color))

    def output_reverse(self, x, y, text, color=0):
        self.win.addstr(y + 1, x + 1, text, curses.color_pair(color) | curses.A_REVERSE)

    def output_bold(self, x, y, text, color=0):
        self.win.addstr(y + 1, x + 1, text, curses.color_pair(color) | curses.A_BOLD)

    def close_window(self):
        if self._win is not None:
            while True:
                key = self.win.getkey()
                if key == 'q': break
            self._win.clear()
            self._win.refresh()
            self._win = None

    def wait_for_key(self):
        self._stdscr.addstr(0, 0, "Press space to continue")
        self._stdscr.refresh()
        while True:
            key = self._stdscr.getkey()
            if key == ' ': break
        self._stdscr.move(0, 0)
        self._stdscr.clrtoeol()
        self._stdscr.refresh()

    def run(self):
        curses.wrapper(self.main)

    def main(self, stdscr):
        self._stdscr = stdscr
        stdscr.clear()
        self._rows, self._cols = stdscr.getmaxyx()
        if self._test_input:
            self._solution.read_test_input()
        else:
            self._solution.read_real_input()
        self.create_window(self.win_width(), self.win_height())
        if (self._part & 0b0001) > 0: self._solution.solve_part_1()
        if (self._part & 0b0010) > 0: self._solution.solve_part_2()
        self.close_window()

    def win_height(self):
        if self._solution.puzzle:
            return len(self._solution.puzzle)
        return 0

    def win_width(self):
        if self._solution.puzzle:
            return len(self._solution.puzzle[0])
        return 0


if __name__ == "__main__":
    animation = Animation(None)
    animation.run()