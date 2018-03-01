import serial 
import time 

class CarControl:
    def __init__(self, device):
        self.arduino_device = device
        self.ser = serial.Serial(self.arduino_device, 9600)
        time.sleep(2)

    def move(self, direction, speed): 
        self.ser.write(int(direction).to_bytes(1, 'big'))
        self.ser.write(int(speed).to_bytes(1, 'big')) #от 0 до 255
        time.sleep(0.0002)

    def turn(self, degree):
        self.ser.write(int(3).to_bytes(1, 'big'))
        self.ser.write(int(degree).to_bytes(1, 'big'))
        time.sleep(0.0002)

    def portDBG(self):
        print(self.ser.readline())

    def __del__(self):
        self.ser.close()
