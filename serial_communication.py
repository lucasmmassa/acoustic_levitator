import time

import numpy as np
import serial
import serial.tools.list_ports

NUMBER_OF_STEPS = 4

ports = serial.tools.list_ports.comports()
print(ports)
first_port = sorted(ports)[0][0]
arduino = serial.Serial(first_port, 115200, timeout=1)
if(not arduino.is_open):
    arduino.open()

def send_message(content, delay=0):
    arduino.write(bytes(content, 'utf-8'))
    time.sleep(delay)
    
def triangular_wave(A):
    aux = []
    aux.append(np.arange(A))
    aux.append(np.arange(A, -A, -1))
    aux.append(np.arange(-A, 0))
    return np.hstack(aux)

    
current = 0
A = 5
u = triangular_wave(A)
f = 0.5
T = 2*np.pi*f
delta_t = T/u.shape[0]

time.sleep(10)
print("START")

i = 0
size = u.shape[0]

x = []
y = []

while True: 
    # for i in range(NUMBER_OF_STEPS):
    #     send_message('+\n', 0.5)
    
    # time.sleep(2)
    
    # for i in range(NUMBER_OF_STEPS):
    #     send_message('-\n', 0.5)
    
    # time.sleep(2)
    
    
    
    
    value = u[i%size]
    if value>current:
        send_message('+\n', delta_t)
    elif value<current:
        send_message('-\n', delta_t)
        
    current = value
    # time.sleep(1)
        
    i += 1
