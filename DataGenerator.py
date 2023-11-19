class DataGenerator():
    def __init__(self, port, baud_rate, debug_flag): 
        if debug_flag:
            pass
        else:
            self.serialconnection = SerialConnection(port, baud_rate)
            

    def getLatestValue(self):
        return 8