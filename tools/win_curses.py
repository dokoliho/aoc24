import curses
import time

def main(stdscr):
    # Farben initialisieren
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    # Clear the screen
    stdscr.clear()

    # Terminalgröße ermitteln
    max_y, max_x = stdscr.getmaxyx()

    # Fenstergröße und Position festlegen
    height, width = 10, 40
    start_y, start_x = (max_y // 2) - (height // 2), (max_x // 2) - (width // 2)

    # Fenster erstellen
    win = curses.newwin(height, width, start_y, start_x)

    # Rahmen zeichnen
    win.border()
    #key = stdscr.getkey()

    # Text im Fenster anzeigen
    win.addstr(1, 1, "Willkommen zu curses!", curses.color_pair(1))
    win.addstr(2, 1, "Drücke 'q', um zu beenden.", curses.color_pair(2))

    # Fenster aktualisieren
    win.refresh()
    time.sleep(1)

    # Warten auf Benutzereingaben
    while True:
        key = win.getkey()
        if key == 'q':
            break
        elif key == 'r':  # Beispiel: Aktualisiere das Fenster bei Taste 'r'
            win.addstr(4, 1, "Taste 'r' gedrückt!", curses.color_pair(1))
            win.refresh()

if __name__ == "__main__":
    curses.wrapper(main)
