import socket
import numpy as np
import cv2
import pickle

PORT = 12000
BUFFER_SIZE = 1024

cap = cv2.VideoCapture(0)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', PORT))

while True:
    # handle client request
    message, address = server_socket.recvfrom(BUFFER_SIZE)
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




    # message, address = server_socket.recvfrom(BUFFER_SIZE)
    # print(address, message, '\n')

    # server_socket.sendto(b'[CC-START]', address)
    # for i in range(5):
    #     server_socket.sendto(b'-Hello-', address)
    # server_socket.sendto(b'[CC-END]', address)
    
        