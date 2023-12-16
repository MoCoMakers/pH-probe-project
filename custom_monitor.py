import argparse
from GraphicalWindow import GraphicalWindow
from DataGenerator import DataGenerator

def main(args):
    try:
        port = args.port
        baud_rate = args.baud_rate
        debug_flag = args.debug_flag

        dataConnection = DataGenerator(port, baud_rate, debug_flag)
        # instance of GraphicalWindow()
        window = GraphicalWindow(dataConnection)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='GUI for pH probe project')
    parser.add_argument('--port', default='COM3')
    parser.add_argument('--baud_rate', default='115200') 
    # a way of accepting true for the value
    parser.add_argument('--debug_flag', action='store_true')
    args = parser.parse_args()
    print("args", args.baud_rate)
    main(args)
