import socket
import curses
import pickle

charset = [' ', '`', '.', ',', '\'', '-', '"', '~', '=', '\u25a1',
           '+', '*', 'm', '%', 'C', '#', 'D', 'B', '@', '\u25bc',
           '\u25A0']

BUFFER_SIZE = 65535

addr = ("127.0.0.1", 12000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(1.0)

frame_data = b''
message = b'hello world!'


def main(stdscr):
    stdscr.clear()
    while True:
        height, width = stdscr.getmaxyx()

        # send request to server: height, width, max pixel value
        message = bytes(str(height) + ',' + str(width) + ',' + str(len(charset)), 'utf-8')
        client_socket.sendto(message, addr)
        try:
            # while True:
            frame_data, server = client_socket.recvfrom(BUFFER_SIZE)

            frame = pickle.loads(frame_data)
            y = 0
            for row in frame:
                x = 0
                for px in row:
                    stdscr.addch(y, x, charset[int(px)])
                    x += 1
                y += 1

            # stdscr.addstr(int(height/2), int(width/2), str((height, width)))

            stdscr.refresh()

            # if message.startswith(b'[CC-START]'):
            #     frame_data = message
            # elif message.endswith(b'[CC-END]'):
            #     frame_data += message

            #     print(server, frame_data)

            #     print('\n', frame_data[10:-8]) # get rid of msg padding
            #     break
            # else:
            #     frame_data += message
        
        except socket.timeout:
            print('REQUEST TIMED OUT')

curses.wrapper(main)
