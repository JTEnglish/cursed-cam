from curses import wrapper
import numpy as np
import cv2

charset = [' ', '.', '-', '=', '\u25a1', '+', '*', '#', '%', '@', '\u25bc', '\u25A0']

def main(stdscr):
    stdscr.clear()

    while True:
        height, width = stdscr.getmaxyx()
        stdscr.addstr(int(height/2), int(width/2), str((height, width)))

        stdscr.refresh()

    # stdscr.getkey()


wrapper(main)
