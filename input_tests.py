import os
import threading
import time
from time import perf_counter

import cv2
import matplotlib.pyplot as plt
import numpy as np
import serial
import serial.tools.list_ports

# arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)
# arduino.write(bytes('+\n', 'utf-8'))

def send_message(content, delay=0):
    arduino.write(bytes(content, 'utf-8'))
    time.sleep(delay)
    
def triangular_wave(A):
    aux = []
    aux.append(np.arange(A))
    aux.append(np.arange(A, -A, -1))
    aux.append(np.arange(-A, 0))
    return np.hstack(aux)

def thread_func():
    current = 0
    time.sleep(2)
    print("START")

    i = 0
    size = u.shape[0]

    input_x = []
    x_values = []
    y_values = []
    
    total = perf_counter()
    
    init = perf_counter()
    
    for i in range(size):  
        value = u[i%size]
        if value>current:
            send_message('-\n', 0)
        elif value<current:
            send_message('+\n', 0)
            
        current = value
        
        diff = perf_counter() - init
        
        time.sleep(delta_t - diff)
        
        global mutex
        with mutex:
            input_x.append(value)
            x_values.append(x)
            y_values.append(y)
        
        init = perf_counter()  
    total = perf_counter() - total
    print('total time:', total)
     
    time.sleep(2)    
    out.release()
    np.save(f'input_tests2/amplitude{A}/input.npy', input_x)
    np.save(f'input_tests2/amplitude{A}/x.npy', x_values)
    np.save(f'input_tests2/amplitude{A}/y.npy', y_values)

    print("FINISHED")

x = None
y = None
mutex = threading.Lock()

A = 10

if not os.path.isdir(f'input_tests2/amplitude{A}'):
    os.mkdir(f'input_tests2/amplitude{A}')

u = triangular_wave(A)
f = 0.5
T = 1/f
delta_t = T/(u.shape[0]+1)


ports = serial.tools.list_ports.comports()
first_port = sorted(ports)[0][0]
arduino = serial.Serial(first_port, 115200, timeout=1)
if(not arduino.is_open):
    arduino.open()

cam = cv2.VideoCapture(0)
img_counter = 0
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(f'input_tests2/amplitude{A}/test.avi', fourcc, 20.0, (640, 480))

fontScale = 1
color = (255, 0, 0)
thickness = 2
org = (10, 25)
font = cv2.FONT_HERSHEY_SIMPLEX

thread = threading.Thread(target=thread_func, args=(), daemon=True)
thread.start()

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    s = hsv[:, :, 1]
    blur = cv2.GaussianBlur(s,(11,11),0)
    _, otsu = cv2.threshold(blur,40,255,cv2.THRESH_BINARY_INV)
    roi_coordinates = np.argwhere(otsu)
    
    with mutex:
        y, x = np.mean(roi_coordinates, axis=0).astype(int)
    
    # print(f'X axis position: {x}')
    
    result = frame.copy()
    result = cv2.circle(result, (x, y), 7, (0, 180, 0), -1)

    cv2.putText(result, f'Coordinates: (x, y) = ({x}, {y})', 
                org, font, fontScale, color, thickness, cv2.LINE_AA)
    
    out.write(result) 

    cv2.imshow("original", result)
    cv2.imshow("s channel", s)
    cv2.imshow("blur", blur)
    cv2.imshow("binary", otsu)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        cv2.imwrite("img/original.png", frame)
        cv2.imwrite("img/s_channel.png", s)
        cv2.imwrite("img/blur.png", blur)
        cv2.imwrite("img/binary.png", otsu)
        cv2.imwrite("img/result.png", result)
    elif k%256 == 99:
        # c pressed
        cv2.imwrite("img/ruler3.png", frame)

cam.release()

cv2.destroyAllWindows()

