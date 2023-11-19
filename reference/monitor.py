import serial
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import logging
from matplotlib.mlab import specgram
from scipy.fftpack import fft
from collections import deque
import os
import time
import sys

logger = logging.getLogger("logger.plot")
logger.setLevel(logging.WARN)

class SerialPlot:

    def __init__(self, str_port, baud_rate, max_len, num_of_sensors, fft_len, ser_instance=False):
        self.__max_len = max_len
        self.__num_of_sensors = num_of_sensors

        """
        self.__ser = serial.Serial(str_port, baud_rate)
        self.__num_of_sensors = num_of_sensors
        """
        
        if not ser_instance:
            # If ser_instance is false, then create serial instance or connection 
            self.__ser = serial.Serial(str_port, baud_rate)
        else:
            # If ser_instance is true, then it is an instance and is no longer a boolean, but an object
            # In Python, objects and non-null strings  
            self.__ser = ser_instance
        self.__ser.flushInput() # e.g. serial.Serial.flushInstance()

        try:
            self.__ser = serial.Serial(str_port, baud_rate)
            # print("self.__ser: ", self.__ser)
            self.__ser.flushInput()
        except:
            # print("AttributeError: 'SerialPlot' object has no attribute '_SerialPlot__ser")
            print("{} not found".format(str_port))
        
        self.__data = [deque([0.0] * max_len) for num in range(num_of_sensors)]
        self.__lock = True
        self.cnt = 0
        self.ti = time.time()
        self.time = 0
        self.ann = None
        self.fft_len = fft_len
        self.__sampling_freq = 25

    def __add_to_buf(self, buf, val):
        if len(buf) < self.__max_len:
            buf.append(val)
        else:
            buf.pop()
            buf.appendleft(val)

    def __add(self, data):
        print("Data is")
        print(data)
        assert (len(data) == self.__num_of_sensors)
        for (rcv_data, deque) in zip(data, self.__data):
            self.__add_to_buf(deque, rcv_data)

    def __get_serial_data(self, p):
        try:
            data = []
            # print("self.__ser:", self.__ser)
            while self.__ser.in_waiting > 0:
                line = self.__ser.readline()
                print("LIne is")
                print(line)
                print(type(line))
                if p == True:
                    print(line.strip().split(b','))
                data = [float(val) for val in line.strip().split(b',')]
                
                print("data (list comprehension): ", data)
                # raise Exception("myMessage")
                
                # data = data[:2]
                self.__add(data)
            return data
        except KeyboardInterrupt:
            print("exitiing")

    def update_raw_data(self, frame, sub_plot):
        #print("sub_plot: ": sub_plot)
        self.__get_serial_data(False)
        min_average = np.inf
        min_plot = None
        # sub_plot[0] is a list of values; in this case, representing the plot variable
        # subplot[1] is a list of values; in this case, representing the axes variable
        # self.__data is a list of raw data of the same length as there are a number of plots
        print("self.__data: ", self.__data)
        print("self.__data: ", self.__data)
        for plot, ax, d in zip(sub_plot[0], sub_plot[1], self.__data):
            plot.set_data(range(self.__max_len), d)
            plot.set_color('b')
            ave = np.average(d)
            ax.set_title("ave={:.2f}".format(ave))
            if (ave < min_average):
                min_average = ave
                min_plot = plot
        min_plot.set_color('r')
        self.__lock = False

    def update_sum_plot(self, plot, ax):
        sum = self.get_sum_buffered_data()
        plot.set_data(range(len(sum)), sum)
        ax.set_title("average = {:.2f}".format(np.average(sum)))
        # ax.grid(color='k', linestyle='--', linewidth=0.5)
        return sum

    def update_fft_plot(self, plot, ax, data, cnt, t):
        fft_data = self.get_fft(data, length=self.fft_len)
        dc = fft_data[0]
        # get maximum from first
        sub_data = list(fft_data[0:int(self.fft_len / 2)])
        max_harmonic = max(sub_data)
        ratio = max_harmonic
        max_harmonic_number = sub_data.index(max_harmonic)
        max_harmonic_freq = self.__sampling_freq * max_harmonic_number * 1.0 / self.fft_len
        plot.set_data(range(len(fft_data)), fft_data)
        ax.set_title("rate={:.2f} f={:.2f} cnt={} t={:.2f}".format(
            ratio, max_harmonic_freq, int(cnt), t))
        if self.ann != None:
            self.ann.remove()
        self.ann = ax.annotate('local max',
                               xy=(max_harmonic_number, max_harmonic),
                               xytext=(max_harmonic_number, max_harmonic + 10),
                               arrowprops=dict(facecolor='red', shrink=0.01),
                               )
        return ratio, max_harmonic_freq

    def update_analyse(self, frame, sub_plot):
        if not self.__lock:
            tim = time.time() - self.ti
            print("tim: ", tim)
            self.ti = time.time()
            print("self.ti", self.ti)
            #os._exit(1)
            sum_array = self.update_sum_plot(sub_plot[0][1], sub_plot[1][1])
            threshold, max_harmonic_freq = self.update_fft_plot(sub_plot[0][0],
                                                                sub_plot[1][0],
                                                                sum_array,
                                                                self.cnt,
                                                                self.time)
            if threshold > 80:
                c = tim * max_harmonic_freq
                self.cnt += c
                self.time = self.time + tim
                logger.debug(c)
            else:
                cnt = 0
            self.__lock = True
    
    def do_update_analyse(self, sp, is_debug):
        # Want to return sp.update_analyse if it makes sense
        # Otherwise, return fake raw data
        if not is_debug:
            raw_output_data = sp.update_analyse
            print("raw_output_data: ", raw_output_data)
            print("type of raw_output_data: ", type(raw_output_data))
            return raw_output_data
        else:
            return self.update_analyse_for_debug
        
    def update_analyse_for_debug(self, frame, sub_plot):
        #if not self.__lock:
        
        #tim = time.time() - self.ti
        tim = 0.004
        #self.ti = time.time()
        sum_array = self.update_sum_plot(sub_plot[0][1], sub_plot[1][1])
        threshold, max_harmonic_freq = self.update_fft_plot(sub_plot[0][0],
                                                            sub_plot[1][0],
                                                            sum_array,
                                                            self.cnt,
                                                            self.time)
        if threshold > 80:
            c = tim * max_harmonic_freq
            self.cnt += c
            self.time = self.time + tim
            logger.debug(c)
        else:
            cnt = 0
            #self.__lock = True
                      
    def get_sum_buffered_data(self):
        sum = []
        for i in range(self.__max_len):
            s = 0
            for d in range(self.__num_of_sensors):
                s = s + self.__data[d][i]
            sum.append(s)
        return sum

    def get_average(selhf):
        return np.average(self.get_sum_buffered_data())

    def get_spectrogram(self, data):
        Pxx, freqs, bins = specgram(data, NFFT=64, Fs=25, noverlap=5)
        return Pxx, freqs, bins

    def get_fft(self, data, length):
        try:
            data = data - np.average(data)
            fft_data = 20 * np.log(np.abs(fft(data, n=length)))
        except:
            pass
        return fft_data

    def add_ma_filter(self, data, ma_len):
        return np.convolve(data, np.ones(ma_len))

    def get_row_data(self):
        return self.__data


class Draw:

    def __init__(self, serial_port, baud, num_of_sensors, fft_length, ser_instance=False, is_debug=False):
        fft_len = fft_length

        if not is_debug:
            
            if not ser_instance:
                try: 
                    print("Oops. I am in here.")
                    sp = SerialPlot("/dev/" + str(serial_port), baud, 25, num_of_sensors,
                                fft_length)
                except:
                    print("I am here!") 
                    sp = SerialPlot("" + str(serial_port), baud, 25, num_of_sensors,
                                fft_length)
            else:
                sp = SerialPlot("", baud, 25, num_of_sensors,
                                fft_length, ser_instance)
        else:
            # Defining the sp variable b/c sp will not exist if there is no physical device connected
            sp = None

        # define fig
        self.rawd_fig, self.rawd_ax = plt.subplots(2, 2)
        self.fft_fig, self.fft_ax = plt.subplots(2, 1)
        self.rawd_plot = []
        self.fft_plot = []
        rawd_color = ['r', 'g', 'b', 'c']
        for c, a in zip(rawd_color, self.rawd_ax.reshape(4, )):
            a.set_xlim([0, 25])
            a.set_ylim([0, 15]) 
            b, = a.plot([], [], color=c)
            self.rawd_plot.append(b)
        fft_label = ['fft', 'sum']
        fft_color = ['g', 'r']
        for l, c, ax in zip(fft_label, fft_color, self.fft_ax):
            ax.set_xlim([0, 25])
            ax.set_ylim([0, 200])
            b, = ax.plot([], [], label=l, color=c)
            self.fft_plot.append(b)

        ax.grid(color='k', linestyle='--', linewidth=0.5)
        self.fft_ax[0].set_xlim([0, fft_len])
        self.fft_ax[0].set_ylim([0, 200])
        b, = self.fft_ax[0].plot([], [], label='fft', color='g')
        self.fft_fig.canvas.manager.set_window_title(
            'FFT len={} & Average'.format(fft_len))
        self.rawd_fig.canvas.manager.set_window_title('Raw Data')

        # Display of 4 Plots
        anim = animation.FuncAnimation(self.rawd_fig, self.do_update_raw_data(sp, is_debug),
                                       fargs=((self.rawd_plot,
                                               self.rawd_ax.reshape(4, )),),
                                       interval=1)
        
        # Display of 2 Plots
        anim1 = animation.FuncAnimation(self.fft_fig, sp.do_update_analyse(sp, is_debug),
                                        fargs=((self.fft_plot, self.fft_ax),),
                                        interval=1)
        
        plt.show()

    def do_update_raw_data(self, sp, is_debug):
        # Want to return sp.update_raw_data if it makes sense
        # Otherwise, return fake raw data
        if not is_debug:
            raw_output_data = sp.update_raw_data
            print("raw_output_data: ", raw_output_data)
            print("type of raw_output_data: ", type(raw_output_data))
            return raw_output_data
        else:
            return update_raw_data_for_debug
         
def main():
    try:
        serial_port = sys.argv[1]
        baud = int(sys.argv[2])
        fft_length = int(sys.argv[3])
        num_of_sensors = 4
        is_debug = sys.argv[4]

        if is_debug.lower() == "true":
            is_debug = True
        else:
            is_debug = False

        d = Draw(serial_port=serial_port, baud=baud,
                 fft_length=fft_length, num_of_sensors=num_of_sensors, is_debug=is_debug)
    except KeyboardInterrupt:
        exit()

# the purpose is to execute same thing with fake raw data
def update_raw_data_for_debug(frame, sub_plot):
        #print("sub_plot: ": sub_plot)
        min_average = np.inf
        min_plot = None
        num_of_sensors = 4
        __data = [deque([0.0] * max_len) for num in range(num_of_sensors)]
        __max_len = 256
        # sub_plot[0] is a list of values; in this case, representing the plot variable
        # subplot[1] is a list of values; in this case, representing the axes variable
        # self.__data is a list of raw data of the same length as there are a number of plots
        for plot, ax, d in zip(sub_plot[0], sub_plot[1], __data):
            plot.set_data(range(__max_len), d)
            plot.set_color('b')
            ave = np.average(d)
            ax.set_title("ave={:.2f}".format(ave))
            if (ave < min_average):
                min_average = ave
                min_plot = plot
        min_plot.set_color('r')
        #self.__lock = False
                   
if __name__ == '__main__':
    main()
