from SerialConnection import SerialConnection

class DataGenerator():
    # need a common function called getLatestData
    def __init__(self, port, baud_rate, debug_flag): 
        self.debug_flag = debug_flag
        self.debugIndex = 0
        # debug_flag is set on original command prompt
        if not self.debug_flag:
            self.serialconnection = SerialConnection(port, baud_rate, debug_flag)
            
    def getNewRandom(self):
        # list hardcoded of all possible hard randoms & incrementally move through it
        possibleValues = [1.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 12.0, 10.0, 8.0, 6.0, 4.0, 2.0]
        # algo. is keeping track of point index and then returning index
        # only place to store persistance storage is original obj. (self)
        self.debugIndex = self.debugIndex+1

        # Know when reach the end of the list then reset the index to 0

        # Use length of possibleValues and use self.debugIndex
        # self.debugIndex: 13 is max index
        # should trigger if index is now 14
        if self.debugIndex >= len(possibleValues): 
            self.debugIndex = 0
        
        # animation is adding a value to the right & shifting to the left

        # calling list of possibleValues as index 
        return possibleValues[self.debugIndex]
    
        #would like x data to be 100 data points so it looks more continuous
    # we are either calling data or getting latest data
    # go back & reread it into the code

    def getLatestValue(self):
        # object has no persistence, except itself.attributes
        if self.debug_flag:
            return self.getNewRandom()
        else:
            """
            calling readLine() from SerialConnection() class
            assume returning a string, so typecast str to float
            """
            return float(self.serialconnection.readLine())
            
          