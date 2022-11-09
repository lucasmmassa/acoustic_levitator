import msvcrt
import threading
from enum import Enum
from time import sleep

import cv2
import matplotlib.pyplot as plt
import numpy as np
import serial
import serial.tools.list_ports

SEND_MESSAGE_DELAY = 0.5 #seconds
TOLERANCE = 1
CAM_INDEX = 1
FONTSCALE = 1
COLOR = (255, 0, 0)
THICKNESS = 2
ORG = (10, 25)
FONT = cv2.FONT_HERSHEY_SIMPLEX

class Directions(Enum):
    MOVE_LEFT = '+\n'
    MOVE_RIGHT = '-\n'

class Controller:
    def __init__(self) -> None:
        self.target = None
        self.current_position = None
        self.delay = SEND_MESSAGE_DELAY
        self.run = True
        self.esp = self.init_esp()
        self.cam = self.init_camera(cam_index=CAM_INDEX)
        self.init_thread()
        
        
    def init_esp(self) -> serial.Serial:
        print('Initializing ESP32...')
        ports = serial.tools.list_ports.comports()
        first_port = sorted(ports)[0][0]
        esp = serial.Serial(first_port, 115200, timeout=1)
        if(not esp.is_open):
            esp.open() 
        print('ESP32 ready.')    
        return esp 
    
    
    def init_camera(self, cam_index) -> cv2.VideoCapture:
        print('Initializing camera...')
        camera = cv2.VideoCapture(cam_index)
        print('Camera ready.')
        return camera
    
    
    def init_thread(self):
        print('Starting controll thread...')
        thread = threading.Thread(target=self.controll_position, args=(), daemon=True)
        thread.start()
        
        
    def set_target(self, target) -> None:
        self.target = target
        
        
    def controll_position(self) -> None:
        while(self.run):
            if self.target and self.current_position:
                with mutex:
                    error = self.target-self.current_position
                    
                if error > 0 and abs(error) > TOLERANCE:
                    self.esp.write(bytes('-\n', 'utf-8'))
                    sleep(self.delay)
                if error < 0 and abs(error) > TOLERANCE:
                    self.esp.write(bytes('+\n', 'utf-8'))
                    sleep(self.delay)
                            

    def work_loop(self) -> None:
        input_buffer = ''
        
        while self.run:
            ret, frame = self.cam.read()
            if not ret:
                self.run = False
                continue            

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            s = hsv[:, :, 1]
            blur = cv2.GaussianBlur(s,(11,11),0)
            _, otsu = cv2.threshold(blur,40,255,cv2.THRESH_BINARY_INV)
            roi_coordinates = np.argwhere(otsu)
            
            if roi_coordinates.shape[0] > 0:
                y, x = np.mean(roi_coordinates, axis=0).astype(int)
            else:
                y = -1
                x = -1
            
            with mutex:
                self.current_position = x
                
            try:
                if msvcrt.kbhit():
                    entry = msvcrt.getch()                    
                    if entry == b'\r':
                        target = int(input_buffer)
                        input_buffer = ''
                        if target == 0:
                            target = None
                        with mutex:
                            self.target = target
                        print('Target set to', self.target)
                                             
                    else:
                        char = entry.decode('utf-8')
                        
                        if char.isnumeric():
                            input_buffer += char
                            print(f'Current buffer: {input_buffer}')
                        
                        if char == 'r':
                            input_buffer = ''
                            print('Buffer reset.')
                        
            except ValueError:
                pass
                            
            result = frame.copy()
            result = cv2.circle(result, (x, y), 7, (0, 180, 0), -1)

            cv2.putText(result, f'Coordinates: (x, y) = ({x}, {y})', 
                        ORG, FONT, FONTSCALE, COLOR, THICKNESS, cv2.LINE_AA)
            
            
            cv2.imshow("original", result)
            # cv2.imshow("s channel", s)
            # cv2.imshow("blur", blur)
            # cv2.imshow("binary", otsu)
            
            _ = cv2.waitKey(1)

        self.cam.release()
        cv2.destroyAllWindows()

            
            

def main():
    controller = Controller()
    controller.work_loop()


mutex = threading.Lock()
        
if __name__ == '__main__':
    main()