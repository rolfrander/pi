#!/usr/bin/python3

#-------------------------------------------------------------------------------
# Name:        MCP3002 Measure 5V
# Purpose:     Measure the 5V Supply of the Raspberry Pi
#
# Author:      paulv
#
# Created:     22-10-2015
# Copyright:   (c) paulv 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import spidev # import the SPI driver
import sys
from time import sleep, perf_counter

DEBUG = False
vref = 3.3 * 1000 # V-Ref in mV (Vref = VDD for the MCP3002)
resolution = 2**10 # for 10 bits of resolution
calibration = 0 # in mV, to make up for the precision of the components

# MCP3008 Control bits
#
#   7   6   5   4   3   2   1   0
#   X   1   S  D0  D1  D2   X   X
#
# bit 6 = Start Bit
# S = SGL or \DIFF SGL = 1 = Single Channel, 0 = \DIFF is pseudo differential
# O = ODD or \SIGN
# in Single Ended Mode (SGL = 1)
#   ODD 0 = CH0 = + GND = - (read CH0)
#       1 = CH1 = + GND = - (read CH1)
# in Pseudo Diff Mode (SGL = 0)
#   ODD 0 = CH0 = IN+, CH1 = IN-
#       1 = CH0 = IN-, CH1 = IN+
#
# M = MSBF
# MSBF = 1 = LSB first format
#        0 = MSB first format
# ------------------------------------------------------------------------------


# SPI setup
spi_max_speed = 1000000 # 1 MHz (1.2MHz = max for 2V7 ref/supply)
# reason is that the ADC input cap needs time to get charged to the input level.
CE = 0 # CE0 | CE1, selection of the SPI device

spi = spidev.SpiDev()
spi.open(0,CE) # Open up the communication to the device
spi.max_speed_hz = spi_max_speed

#
# create a function that sets the configuration parameters and gets the results
# from the MCP3002
#
def read_mcp3008(channel):
    cmd = 0b01100000 | (channel << 2)

    if DEBUG : print("cmd = ", cmd)

    spi_data = spi.xfer2([cmd,0, 0]) # send hi_byte, low_byte; receive hi_byte, low_byte

    if DEBUG : print("Raw ADC (hi-byte, low_byte) = {}".format(spi_data))

    # receive data range: 000..3FF (10 bits)
    # MSB first: (set control bit in cmd for LSB first)
    # spidata[0] =  X,  X,  X,  X,  X,  0, B9, B8
    # spidata[1] = B7, B6, B5, B4, B3, B2, B1, B0
    # LSB: mask all but B9 & B8, shift to left and add to the MSB
    adc_data = (spi_data[1] << 2) + ((spi_data[2] & 0b11000000) >> 6)
    return adc_data


try:
    print("MCP3002 Single Ended CH0 Read of the 5V Pi Supply")
    print("SPI max sampling speed = {}".format(spi_max_speed))
    print("V-Ref = {0}, Resolution = {1}".format(vref, resolution))
    print("SPI device = {0}".format(CE))
    print("-----------------------------\n")

    collecting = False
    waiting = True
    counter = 0
    scaling = 3
    graphsize = 300
    samplecount = graphsize * scaling
    data = [0]*samplecount
    starttime = 0
    while True:
        # average three readings to get a more stable one
        #channeldata_1 = read_mcp3008(0) # get CH0 input
        #sleep(2)
        #channeldata_2 = read_mcp3008(0) # get CH0 input
        #sleep(2)
        #channeldata_3 = read_mcp3008(0) # get CH0 input
        #channeldata = (channeldata_1+channeldata_2+channeldata_3)/3
        #
        channeldata = read_mcp3008(1)
        # Voltage = (CHX data * (V-ref [= 3300 mV] * 2 [= 1:2 input divider]) / 1024 [= 10bit resolution]
        #

        if collecting:
            #print("Value: {}".format(channeldata))
            data[counter] = channeldata
            counter += 1

            if (counter >= samplecount):
                elapsed_time = perf_counter() - starttime
                print("Elapsed time: ", elapsed_time*1000, "ms")
                print("Time resolution: ", elapsed_time*1000/samplecount, "ms")
                print("Output scaling factor: ", scaling)
                collecting = False
                for i in range(64, 0, -1):
                    for x in range(graphsize):
                        # average "scaling" number of samples
                        d = 0
                        for di in range(scaling):
                            d += data[di+x*scaling]
                        d = int(d/scaling)
                        if (d >> 4) >= i:
                            sys.stdout.write(":")
                        else:
                            sys.stdout.write(" ")
                    sys.stdout.write("\n")
                    sys.stdout.flush()
        else:
            if waiting and (channeldata > 100):
                collecting = True
                waiting = False
                counter = 0
                print("Start measurement:")
                starttime = perf_counter()
            if channeldata < 100:
                waiting = True

            sleep(0.0)

except KeyboardInterrupt: # Ctrl-C
    if DEBUG : print ("Closing SPI channel")
    spi.close()

def main():
    pass

if __name__ == '__main__':
    main()
