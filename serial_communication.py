import time

import serial

NUMBER_OF_STEPS = 4
arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)

def send_message(content, delay=0):
    arduino.write(bytes(content, 'utf-8'))
    time.sleep(delay)
    

while True: 
    for i in range(NUMBER_OF_STEPS):
        send_message('+\n', 0.5)
    
    time.sleep(2)
    
    for i in range(NUMBER_OF_STEPS):
        send_message('-\n', 0.5)
    
    time.sleep(2)
    