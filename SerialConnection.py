import serial

class SerialConnection():
    def __init__(self, port, baud_rate, debug_flag):
        self.serial = serial.Serial(port, baud_rate)
        self.port = port
        self.baud_rate = baud_rate
        self.debug_flag = debug_flag
        
    def readLine(self):
        # assume there is a connection
        line = self.serial.readline()
        return line