#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import serial
import os
import time

##
# This class runs a thread which sends the serial packets.
class SerialSender:

    ##
    # Tries to use the ttyAMA0 connection. If it is not availible the class will run in a debug mode which is
    # not actually sending packages.
    #
    # @param message_queue The synchronized message queue to communicate with the Server class
    def __init__(self, message_queue):
        print("SerialSender started")

        os.system("stty -F /dev/ttyAMA0 115200") #configs the system to allow use of tty
        os.system("exec 9> /dev/ttyAMA0")

        self.message_queue = message_queue
        try:
            self.port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=1.0)
            self.debug = False
        except OSError:
            print(
                "/dev/ttyAMA0 was not found. Looks like you are testing on your computer, sending of serials was disabled",
                file=sys.stderr)
            self.debug = True

    ##
    # The thread function which sends the packets.
    #
    # @param args: Not used, only needed because of python standards
    # @param args2: Not used, only needed because of python standards
    def run(self, args, args2):
        while True:
            number, protocol, time_between = self.message_queue.get(True)

            last_packet_time = 0
            sended_packets = 0
            print("serial sender got %d %d %d", (number, protocol, time_between))
            while sended_packets < number:
                if time.time() > last_packet_time + (time_between / 1000):
                    if not self.debug:
                        if protocol == 0:
                            print("send UART")
                            self.port.write(bytes("A", 'UTF-8'))
                        elif protocol == 1:
                            print("send SPI")
                            os.system("./spidev_test -D /dev/spidev0.0")
                        else: #I2C
                            pass #TODO
                    else:
                        print("pseudo sended a serial packet", file=sys.stderr)
                    last_packet_time = time.time()
                    sended_packets += 1