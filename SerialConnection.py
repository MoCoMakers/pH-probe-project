import serial

class SerialConnection():
    def __init__(self, port, baud_rate, debug_flag):
        self.serial = serial.Serial(port, baud_rate, timeout=1.0) # when do want the error out to happen
        self.port = port
        self.baud_rate = baud_rate
        self.debug_flag = debug_flag
        
    def write(self, data):
        lengths_bytes_written = self.serial.write(data)
        return lengths_bytes_written
        
    def readLine(self):
        # assume there is a connection
        print("Before")
        # why does readline() never read the end
        line = self.serial.readline() # using a serial connection
        print("Line: ", line)
        print("After")
        return line