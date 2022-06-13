import numpy as np
import cv2
import matplotlib.pyplot as plt

cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

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
    frame = cv2.circle(frame, (x, y), 7, (0, 180, 0), -1)

    cv2.imshow("original", frame)
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
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()