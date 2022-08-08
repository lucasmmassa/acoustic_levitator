import serial
import serial.tools.list_ports

ser = None
state = 0

while True:
    if(state == 0):
        try:
            ports = serial.tools.list_ports.comports()
            print(ports)
            first_port = sorted(ports)[0][0]
            ser = serial.Serial(first_port, 115200, timeout=1)
            if(not ser.is_open):
                ser.open()
            if(ser.is_open):
                state = 1
        except:
            print("Connection to microcontroller failed")

    if(state == 1):
        try:    
                ser.write(bytes('+\n', 'utf-8'))

                microcontroller_output = str(ser.readline())
                while microcontroller_output == "b\'\'":
                    microcontroller_output = str(ser.readline())
                print(microcontroller_output)
        except:
             state = 0