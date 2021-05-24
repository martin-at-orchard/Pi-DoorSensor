#!/usr/bin/python3

###########################################################
#
# Door sensor for Cates A
#
# Author: Martin Wedepohl <martin@orchardrecovery.com>
#
###########################################################

import time
import threading
import RPi.GPIO as GPIO
from db import DB
from gpiohandler import GPIOHandler
from queue import Queue
from datetime import datetime
from display import Display
from beep import Beep
from monitordoors import MonitorDoors

###########################################################
#
# Call back function to process the door interrupt
#
# param: id      The id of the GPIO pin causing the interrupt
# param: state   The state of the GPIO pin
# param: txQueue The transmit queue to fill
#
###########################################################
def real_cb(id, state, txQueue):
    now = datetime.now()
    txQueue.put([id, state, now])

###########################################################
#
# Main program
#
###########################################################
txQueue = Queue()

# Enable GPIO pin numbering
GPIO.setmode(GPIO.BOARD)

database = DB()
roomData = database.getRooms()
displayData = []

for id, name, pin in roomData:
   GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
   handler = GPIOHandler(pin, id, real_cb, txQueue, edge=GPIO.BOTH, bouncetime=200)
   handler.start()
   displayData.append([id, name, handler.lastPinVal()])
   GPIO.add_event_detect(pin, GPIO.BOTH, callback = handler)

gpioDirty = True

# Curses display setup
display = Display(0, 0, 'Closed', ' OPEN ')
display.run()
display.setup(displayData)
beepLock = threading.Lock()
monitorDoors = MonitorDoors(txQueue, beepLock, display)

try:
    monitorDoors.run()
    while(True):
        pass

except KeyboardInterrupt:
    GPIO.cleanup()
    display.cleanup()
    gpioDirty = False

except Exception as e:
    GPIO.cleanup()
    display.cleanup()
    gpioDirty = False

if gpioDirty:
    GPIO.cleanup()
    display.cleanup()

print("Exiting door sensor program")
