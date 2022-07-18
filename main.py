import time

import cv2
import matplotlib.pyplot as plt
import numpy as np
import serial

# arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)
# arduino.write(bytes('+\n', 'utf-8'))

cam = cv2.VideoCapture(0)
img_counter = 0

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
    y, x = np.mean(roi_coordinates, axis=0).astype(int)
    result = frame.copy()
    result = cv2.circle(result, (x, y), 7, (0, 180, 0), -1)

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
