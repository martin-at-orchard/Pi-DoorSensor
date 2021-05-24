#!/usr/bin/python3

###########################################################
#
# GPIO pin handler
#
# Author: Martin Wedepohl <martin@orchardrecovery.com>
#
###########################################################

import time
import threading
import RPi.GPIO as GPIO

###########################################################
#
# Class for the GPIO handler, will perform software debouncing
#
###########################################################
class GPIOHandler(threading.Thread):

    #######################################################
    #
    # Class initialization
    #
    # Calls the parent class
    # Sets up the class arguments, saves the current door
    # state and initializes the thread lock.
    #
    # param: self       This class
    # param: pin        The GPIO pin
    # param: func       The callback function
    # param: txQueue    The transmit queue
    # param: edge       The edge (FALLING, RISING, BOTH) - Default BOTH
    # param: bouncetime The bounce time in mSecs - Default 200mSec
    #
    #######################################################
    def __init__(self, pin, id, func, txQueue, edge=GPIO.BOTH, bouncetime=200):

        super().__init__(daemon=True)

        self.pin = pin
        self.id = id
        self.func = func
        self.txQueue = txQueue
        self.edge = edge
        self.bouncetime = float(bouncetime)/1000
        self.lastpinval = GPIO.input(self.pin)
        self.lock = threading.Lock()

    #######################################################
    #
    # Interrupt handler for the class.
    #
    # Attempt to aquire the thread lock,
    # return immediately if the aquire it fails.
    #
    # If the aquire succeeds start a timer to debounce the
    # door. When the timeer expires call the read function.
    #
    # param: self    This class
    # param: args[0] The GPIO pin causing the interrupt
    #
    #######################################################
    def __call__(self, *args):

        if not self.lock.acquire(blocking=False):
            return

        t = threading.Timer(self.bouncetime, self.read, args=args)
        t.start()

    #######################################################
    #
    # Read the state of the GPIO pin attached to the door.
    #
    # Only call the actual callback function if:
    #   - Going from 0 to 1 and edge detect falling or both
    #   - Going from 1 to 0 and edge detect rising or both
    #
    # Ensure the debounce lock is released.
    #
    # param: self    This class
    # param: args[0] The GPIO pin causing the interrupt
    #
    #######################################################
    def read(self, *args):

        pinval = GPIO.input(self.pin)

        if (((0 == pinval and 1 == self.lastpinval) and (self.edge in [GPIO.FALLING, GPIO.BOTH])) or
            ((1 == pinval and 0 == self.lastpinval) and (self.edge in [GPIO.RISING, GPIO.BOTH]))):
            self.func(self.id, pinval, self.txQueue)

        self.lastpinval = pinval
        self.lock.release()

    #######################################################
    #
    # Return the last pin value
    #
    # param: self This class
    #
    # return: The value of the last pin reading
    #
    #######################################################
    def lastPinVal(self):
        return self.lastpinval
