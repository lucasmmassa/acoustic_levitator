import time
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
    

while True: 
    for i in range(NUMBER_OF_STEPS):
        send_message('+\n', 0.01)
    
    time.sleep(0.5)
    
    for i in range(NUMBER_OF_STEPS):
        send_message('-\n', 0.01)
    
    time.sleep(0.5)
    