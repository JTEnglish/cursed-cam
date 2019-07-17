import socket
import curses
import pickle
import numpy as np
import cv2
import threading
import sys

charset = [' ', '`', '.', ',', '\'', '-', '"', '~', '=', '\u25a1',
           '+', '*', 'm', '%', 'C', '#', 'D', 'B', '@', '\u25bc',
           '\u25A0']

CLIENT_BUFFER_SIZE = 65535
SERVER_PORT = 12000
SERVER_BUFFER_SIZE = 1024

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(1.0)

def cam_server():
    cap = cv2.VideoCapture(0)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', SERVER_PORT))

    while True:
        # handle client request
        message, address = server_socket.recvfrom(SERVER_BUFFER_SIZE)
        msg = str(message)[2:-1].split(',') # get string data
        # convert to ints
        height = int(msg[0])
        width = int(msg[1])
        max_pixel = int(msg[2])

        # get webcam frame
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized_image = cv2.resize(gray, (width - 1, height - 1))

        output = np.interp(resized_image, (0, 255), (0, max_pixel - 1))
        server_socket.sendto(pickle.dumps(output), address)

def main(stdscr):
    server_thread = threading.Thread(target=cam_server)
    server_thread.start()

    other_addr = (sys.argv[1], int(sys.argv[2]))

    stdscr.clear()
    while True:
        height, width = stdscr.getmaxyx()

        # send request to server: height, width, max pixel value
        message = bytes(str(height) + ',' + str(width) + ',' + str(len(charset)), 'utf-8')
        client_socket.sendto(message, other_addr)
        try:
            # while True:
            frame_data, server = client_socket.recvfrom(CLIENT_BUFFER_SIZE)

            frame = pickle.loads(frame_data)
            y = 0
            for row in frame:
                x = 0
                for px in row:
                    stdscr.addch(y, x, charset[int(px)])
                    x += 1
                y += 1

            stdscr.refresh()
        
        except socket.timeout:
            print('REQUEST TIMED OUT')

curses.wrapper(main)
