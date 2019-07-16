import curses
import numpy as np
import cv2

charset = [' ', '`', '.', ',', '\'', '-', '"', '~', '=', '\u25a1',
           '+', '*', 'm', '%', 'C', '#', 'D', 'B', '@', '\u25bc',
           '\u25A0']
cap = cv2.VideoCapture(0)

def main(stdscr):
    stdscr.clear()

    while True:
        height, width = stdscr.getmaxyx()
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized_image = cv2.resize(gray, (width - 1, height - 1))

        output = np.interp(resized_image, (0, 255), (0, len(charset) - 1))
        y = 0
        for row in output:
            x = 0
            for px in row:
                stdscr.addch(y, x, charset[int(px)])
                x += 1
            y += 1

        # stdscr.addstr(int(height/2), int(width/2), str((height, width)))

        stdscr.refresh()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            return

    # stdscr.getkey()


curses.wrapper(main)
