#!/usr/bin/python3
#
# Function to handle the door switches
#
# Author:  Martin Wedepohl <martin@orchardrecovery.com>
#
######################################################

######################################################
# Module Imports
######################################################
import RPi.GPIO as GPIO
import time
import curses
import threading
import json
import subprocess

######################################################
# Function Imports
######################################################
from rooms import getrooms
from rooms import updateresults
from datetime import datetime

######################################################
# Global lists and variables
######################################################
rids = []
pins = []
rooms = []
ids = []
states = []
offsetX = 0
offsetY = 0
writeDb = False
bounceTime = 500

stdscr = None

dbLock = None
beepLock = None

######################################################
# Beep Threading class
######################################################


class sensorBeep(threading.Thread):
    def __init__(self, state):
        threading.Thread.__init__(self)
        self.state = state

    def run(self):
        global beepLock

        if ' OPEN ' == self.state:
            if False == beepLock.locked():
                beepLock.acquire(False)

                if True == beepLock.locked():
                    subprocess.run([ 'mpg123', 'open_beep.mp3'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    beepLock.release()

######################################################
# Database Update Threading class
######################################################


class updateDb(threading.Thread):
    def __init__(self, room, status, date):
        threading.Thread.__init__(self)
        self.room = room
        self.status = status
        self.date = date

    def run(self):
        global dbLock
        global rids
        dbLock.acquire()
        updateresults(rids[self.room], self.status, self.date)
        dbLock.release()

######################################################
# Setup GPIO
######################################################


def setupGPIO():
    global pins
    global states
    global bounceTime

    # We are using GPIO pin numbering
    GPIO.setmode(GPIO.BOARD)

    # Loop through all the pins
    # Set the time and read the current state of the switch
    numPins = len(pins)
    for i in range(numPins):
        GPIO.setup(pins[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        if 1 == i:
            GPIO.add_event_detect(pins[i], GPIO.BOTH, callback=buttonStateChanged1, bouncetime=bounceTime)
        elif 2 == i:
            GPIO.add_event_detect(pins[i], GPIO.BOTH, callback=buttonStateChanged2, bouncetime=bounceTime)
        elif 3 == i:
            GPIO.add_event_detect(pins[i], GPIO.BOTH, callback=buttonStateChanged3, bouncetime=bounceTime)
        elif 4 == i:
            GPIO.add_event_detect(pins[i], GPIO.BOTH, callback=buttonStateChanged4, bouncetime=bounceTime)
        elif 5 == i:
            GPIO.add_event_detect(pins[i], GPIO.BOTH, callback=buttonStateChanged5, bouncetime=bounceTime)
        elif 6 == i:
            GPIO.add_event_detect(pins[i], GPIO.BOTH, callback=buttonStateChanged6, bouncetime=bounceTime)
        elif 7 == i:
            GPIO.add_event_detect(pins[i], GPIO.BOTH, callback=buttonStateChanged7, bouncetime=bounceTime)
        elif 8 == i:
            GPIO.add_event_detect(pins[i], GPIO.BOTH, callback=buttonStateChanged8, bouncetime=bounceTime)
        elif 9 == i:
            GPIO.add_event_detect(pins[i], GPIO.BOTH, callback=buttonStateChanged9, bouncetime=bounceTime)
        elif 10 == i:
            GPIO.add_event_detect(pins[i], GPIO.BOTH, callback=buttonStateChanged10, bouncetime=bounceTime)
        elif 11 == i:
            GPIO.add_event_detect(pins[i], GPIO.BOTH, callback=buttonStateChanged11, bouncetime=bounceTime)
        elif 12 == i:
            GPIO.add_event_detect(pins[i], GPIO.BOTH, callback=buttonStateChanged12, bouncetime=bounceTime)
        elif 13 == i:
            GPIO.add_event_detect(pins[i], GPIO.BOTH, callback=buttonStateChanged13, bouncetime=bounceTime)
        elif 14 == i:
            GPIO.add_event_detect(pins[i], GPIO.BOTH, callback=buttonStateChanged14, bouncetime=bounceTime)
        elif 15 == i:
            GPIO.add_event_detect(pins[i], GPIO.BOTH, callback=buttonStateChanged15, bouncetime=bounceTime)
        elif 16 == i:
            GPIO.add_event_detect(pins[i], GPIO.BOTH, callback=buttonStateChanged16, bouncetime=bounceTime)
        elif 17 == i:
            GPIO.add_event_detect(pins[i], GPIO.BOTH, callback=buttonStateChanged17, bouncetime=bounceTime)
        elif 18 == i:
            GPIO.add_event_detect(pins[i], GPIO.BOTH, callback=buttonStateChanged18, bouncetime=bounceTime)

        states[i] = GPIO.input(pins[i])

######################################################
# Initialize the display with the rooms and initial states
######################################################


def initializeDisplay():
    global pins
    global rooms
    global states
    global stdscr
    global offsetX
    global offsetY

    numPins = len(pins)

    for i in range(numPins):
        room = rooms[i]
        ftime = datetime.now()
        ftime = ftime.strftime("%Y-%m-%d %H:%M:%S")
        if (0 == states[i]):
            state = 'Closed'
            attr = curses.color_pair(2)
        else:
            state = ' OPEN '
            attr = curses.color_pair(1) | curses.A_BOLD

        stdscr.addstr(i + offsetY,  0 + offsetX, room)
        stdscr.addstr(i + offsetY, 20 + offsetX, state, attr)
        stdscr.addstr(i + offsetY, 30 + offsetX, ftime)

    stdscr.refresh()

######################################################
# Called when there is a change to the state of a GPIO input
# This uses curses to display the data on the screen
# There needs to be 1 function for each pin?
######################################################

######################################################
# Pin 1
######################################################

def buttonStateChanged1(pin):
    global pins
    global rooms
    global states
    global stdscr
    global offsetX
    global offsetY
    global writeDb

    time.sleep(.1)
    state = GPIO.input(pin)
    i = pins.index(pin)
    if state is not states[i]:
        states[i] = state
        ftime = datetime.now()
        ftime = ftime.strftime("%Y-%m-%d %H:%M:%S")
        status = state
        if (0 == state):
            state = 'Closed'
            attr = curses.color_pair(2)
        else:
            state = ' OPEN '
            attr = curses.color_pair(1) | curses.A_BOLD
        stdscr.addstr(i + offsetY, 20 + offsetX, state, attr)
        stdscr.addstr(i + offsetY, 30 + offsetX, ftime)
        stdscr.refresh()

        if True == writeDb:
            doUpdateDb = updateDb(i, status, ftime)
            doUpdateDb.start()

        doBeep = sensorBeep(state)
        doBeep.start()

######################################################
# Pin 2
######################################################

def buttonStateChanged2(pin):
    global pins
    global rooms
    global states
    global stdscr
    global offsetX
    global offsetY
    global writeDb

    time.sleep(.1)
    state = GPIO.input(pin)
    i = pins.index(pin)
    if state is not states[i]:
        states[i] = state
        ftime = datetime.now()
        ftime = ftime.strftime("%Y-%m-%d %H:%M:%S")
        status = state
        if (0 == state):
            state = 'Closed'
            attr = curses.color_pair(2)
        else:
            state = ' OPEN '
            attr = curses.color_pair(1) | curses.A_BOLD
        stdscr.addstr(i + offsetY, 20 + offsetX, state, attr)
        stdscr.addstr(i + offsetY, 30 + offsetX, ftime)
        stdscr.refresh()

        if True == writeDb:
            doUpdateDb = updateDb(i, status, ftime)
            doUpdateDb.start()

        doBeep = sensorBeep(state)
        doBeep.start()

######################################################
# Pin 3
######################################################

def buttonStateChanged3(pin):
    global pins
    global rooms
    global states
    global stdscr
    global offsetX
    global offsetY
    global writeDb

    time.sleep(.1)
    state = GPIO.input(pin)
    i = pins.index(pin)
    if state is not states[i]:
        states[i] = state
        ftime = datetime.now()
        ftime = ftime.strftime("%Y-%m-%d %H:%M:%S")
        status = state
        if (0 == state):
            state = 'Closed'
            attr = curses.color_pair(2)
        else:
            state = ' OPEN '
            attr = curses.color_pair(1) | curses.A_BOLD
        stdscr.addstr(i + offsetY, 20 + offsetX, state, attr)
        stdscr.addstr(i + offsetY, 30 + offsetX, ftime)
        stdscr.refresh()

        if True == writeDb:
            doUpdateDb = updateDb(i, status, ftime)
            doUpdateDb.start()

        doBeep = sensorBeep(state)
        doBeep.start()

######################################################
# Pin 4
######################################################

def buttonStateChanged4(pin):
    global pins
    global rooms
    global states
    global stdscr
    global offsetX
    global offsetY
    global writeDb

    time.sleep(.1)
    state = GPIO.input(pin)
    i = pins.index(pin)
    if state is not states[i]:
        states[i] = state
        ftime = datetime.now()
        ftime = ftime.strftime("%Y-%m-%d %H:%M:%S")
        status = state
        if (0 == state):
            state = 'Closed'
            attr = curses.color_pair(2)
        else:
            state = ' OPEN '
            attr = curses.color_pair(1) | curses.A_BOLD
        stdscr.addstr(i + offsetY, 20 + offsetX, state, attr)
        stdscr.addstr(i + offsetY, 30 + offsetX, ftime)
        stdscr.refresh()

        if True == writeDb:
            doUpdateDb = updateDb(i, status, ftime)
            doUpdateDb.start()

        doBeep = sensorBeep(state)
        doBeep.start()

######################################################
# Pin 5
######################################################

def buttonStateChanged5(pin):
    global pins
    global rooms
    global states
    global stdscr
    global offsetX
    global offsetY
    global writeDb

    time.sleep(.1)
    state = GPIO.input(pin)
    i = pins.index(pin)
    if state is not states[i]:
        states[i] = state
        ftime = datetime.now()
        ftime = ftime.strftime("%Y-%m-%d %H:%M:%S")
        status = state
        if (0 == state):
            state = 'Closed'
            attr = curses.color_pair(2)
        else:
            state = ' OPEN '
            attr = curses.color_pair(1) | curses.A_BOLD
        stdscr.addstr(i + offsetY, 20 + offsetX, state, attr)
        stdscr.addstr(i + offsetY, 30 + offsetX, ftime)
        stdscr.refresh()

        if True == writeDb:
            doUpdateDb = updateDb(i, status, ftime)
            doUpdateDb.start()

        doBeep = sensorBeep(state)
        doBeep.start()

######################################################
# Pin 6
#####################################################

def buttonStateChanged6(pin):
    global pins
    global rooms
    global states
    global stdscr
    global offsetX
    global offsetY
    global writeDb

    time.sleep(.1)
    state = GPIO.input(pin)
    i = pins.index(pin)
    if state is not states[i]:
        states[i] = state
        ftime = datetime.now()
        ftime = ftime.strftime("%Y-%m-%d %H:%M:%S")
        status = state
        if (0 == state):
            state = 'Closed'
            attr = curses.color_pair(2)
        else:
            state = ' OPEN '
            attr = curses.color_pair(1) | curses.A_BOLD
        stdscr.addstr(i + offsetY, 20 + offsetX, state, attr)
        stdscr.addstr(i + offsetY, 30 + offsetX, ftime)
        stdscr.refresh()

        if True == writeDb:
            doUpdateDb = updateDb(i, status, ftime)
            doUpdateDb.start()

        doBeep = sensorBeep(state)
        doBeep.start()

######################################################
# Pin 7
######################################################

def buttonStateChanged7(pin):
    global pins
    global rooms
    global states
    global stdscr
    global offsetX
    global offsetY
    global writeDb

    time.sleep(.1)
    state = GPIO.input(pin)
    i = pins.index(pin)
    if state is not states[i]:
        states[i] = state
        ftime = datetime.now()
        ftime = ftime.strftime("%Y-%m-%d %H:%M:%S")
        status = state
        if (0 == state):
            state = 'Closed'
            attr = curses.color_pair(2)
        else:
            state = ' OPEN '
            attr = curses.color_pair(1) | curses.A_BOLD
        stdscr.addstr(i + offsetY, 20 + offsetX, state, attr)
        stdscr.addstr(i + offsetY, 30 + offsetX, ftime)
        stdscr.refresh()

        if True == writeDb:
            doUpdateDb = updateDb(i, status, ftime)
            doUpdateDb.start()

        doBeep = sensorBeep(state)
        doBeep.start()

######################################################
# Pin 8
######################################################

def buttonStateChanged8(pin):
    global pins
    global rooms
    global states
    global stdscr
    global offsetX
    global offsetY
    global writeDb

    time.sleep(.1)
    state = GPIO.input(pin)
    i = pins.index(pin)
    if state is not states[i]:
        states[i] = state
        ftime = datetime.now()
        ftime = ftime.strftime("%Y-%m-%d %H:%M:%S")
        status = state
        if (0 == state):
            state = 'Closed'
            attr = curses.color_pair(2)
        else:
            state = ' OPEN '
            attr = curses.color_pair(1) | curses.A_BOLD
        stdscr.addstr(i + offsetY, 20 + offsetX, state, attr)
        stdscr.addstr(i + offsetY, 30 + offsetX, ftime)
        stdscr.refresh()

        if True == writeDb:
            doUpdateDb = updateDb(i, status, ftime)
            doUpdateDb.start()

        doBeep = sensorBeep(state)
        doBeep.start()

######################################################
# Pin 9
######################################################

def buttonStateChanged9(pin):
    global pins
    global rooms
    global states
    global stdscr
    global offsetX
    global offsetY
    global writeDb

    time.sleep(.1)
    state = GPIO.input(pin)
    i = pins.index(pin)
    if state is not states[i]:
        states[i] = state
        ftime = datetime.now()
        ftime = ftime.strftime("%Y-%m-%d %H:%M:%S")
        status = state
        if (0 == state):
            state = 'Closed'
            attr = curses.color_pair(2)
        else:
            state = ' OPEN '
            attr = curses.color_pair(1) | curses.A_BOLD
        stdscr.addstr(i + offsetY, 20 + offsetX, state, attr)
        stdscr.addstr(i + offsetY, 30 + offsetX, ftime)
        stdscr.refresh()

        if True == writeDb:
            doUpdateDb = updateDb(i, status, ftime)
            doUpdateDb.start()

        doBeep = sensorBeep(state)
        doBeep.start()

######################################################
# Pin 10
######################################################

def buttonStateChanged10(pin):
    global pins
    global rooms
    global states
    global stdscr
    global offsetX
    global offsetY
    global writeDb

    time.sleep(.1)
    state = GPIO.input(pin)
    i = pins.index(pin)
    if state is not states[i]:
        states[i] = state
        ftime = datetime.now()
        ftime = ftime.strftime("%Y-%m-%d %H:%M:%S")
        status = state
        if (0 == state):
            state = 'Closed'
            attr = curses.color_pair(2)
        else:
            state = ' OPEN '
            attr = curses.color_pair(1) | curses.A_BOLD
        stdscr.addstr(i + offsetY, 20 + offsetX, state, attr)
        stdscr.addstr(i + offsetY, 30 + offsetX, ftime)
        stdscr.refresh()

        if True == writeDb:
            doUpdateDb = updateDb(i, status, ftime)
            doUpdateDb.start()

        doBeep = sensorBeep(state)
        doBeep.start()

######################################################
# Pin 11
######################################################

def buttonStateChanged11(pin):
    global pins
    global rooms
    global states
    global stdscr
    global offsetX
    global offsetY
    global writeDb

    time.sleep(.1)
    state = GPIO.input(pin)
    i = pins.index(pin)
    if state is not states[i]:
        states[i] = state
        ftime = datetime.now()
        ftime = ftime.strftime("%Y-%m-%d %H:%M:%S")
        status = state
        if (0 == state):
            state = 'Closed'
            attr = curses.color_pair(2)
        else:
            state = ' OPEN '
            attr = curses.color_pair(1) | curses.A_BOLD
        stdscr.addstr(i + offsetY, 20 + offsetX, state, attr)
        stdscr.addstr(i + offsetY, 30 + offsetX, ftime)
        stdscr.refresh()

        if True == writeDb:
            doUpdateDb = updateDb(i, status, ftime)
            doUpdateDb.start()

        doBeep = sensorBeep(state)
        doBeep.start()

######################################################
# Pin 12
######################################################

def buttonStateChanged12(pin):
    global pins
    global rooms
    global states
    global stdscr
    global offsetX
    global offsetY
    global writeDb

    time.sleep(.1)
    state = GPIO.input(pin)
    i = pins.index(pin)
    if state is not states[i]:
        states[i] = state
        ftime = datetime.now()
        ftime = ftime.strftime("%Y-%m-%d %H:%M:%S")
        status = state
        if (0 == state):
            state = 'Closed'
            attr = curses.color_pair(2)
        else:
            state = ' OPEN '
            attr = curses.color_pair(1) | curses.A_BOLD
        stdscr.addstr(i + offsetY, 20 + offsetX, state, attr)
        stdscr.addstr(i + offsetY, 30 + offsetX, ftime)
        stdscr.refresh()

        if True == writeDb:
            doUpdateDb = updateDb(i, status, ftime)
            doUpdateDb.start()

        doBeep = sensorBeep(state)
        doBeep.start()

######################################################
# Pin 13
######################################################

def buttonStateChanged13(pin):
    global pins
    global rooms
    global states
    global stdscr
    global offsetX
    global offsetY
    global writeDb

    time.sleep(.1)
    state = GPIO.input(pin)
    i = pins.index(pin)
    if state is not states[i]:
        states[i] = state
        ftime = datetime.now()
        ftime = ftime.strftime("%Y-%m-%d %H:%M:%S")
        status = state
        if (0 == state):
            state = 'Closed'
            attr = curses.color_pair(2)
        else:
            state = ' OPEN '
            attr = curses.color_pair(1) | curses.A_BOLD
        stdscr.addstr(i + offsetY, 20 + offsetX, state, attr)
        stdscr.addstr(i + offsetY, 30 + offsetX, ftime)
        stdscr.refresh()

        if True == writeDb:
            doUpdateDb = updateDb(i, status, ftime)
            doUpdateDb.start()

        doBeep = sensorBeep(state)
        doBeep.start()

######################################################
# Pin 14
######################################################

def buttonStateChanged14(pin):
    global pins
    global rooms
    global states
    global stdscr
    global offsetX
    global offsetY
    global writeDb

    time.sleep(.1)
    state = GPIO.input(pin)
    i = pins.index(pin)
    if state is not states[i]:
        states[i] = state
        ftime = datetime.now()
        ftime = ftime.strftime("%Y-%m-%d %H:%M:%S")
        status = state
        if (0 == state):
            state = 'Closed'
            attr = curses.color_pair(2)
        else:
            state = ' OPEN '
            attr = curses.color_pair(1) | curses.A_BOLD
        stdscr.addstr(i + offsetY, 20 + offsetX, state, attr)
        stdscr.addstr(i + offsetY, 30 + offsetX, ftime)
        stdscr.refresh()

        if True == writeDb:
            doUpdateDb = updateDb(i, status, ftime)
            doUpdateDb.start()

        doBeep = sensorBeep(state)
        doBeep.start()

######################################################
# Pin 15
######################################################

def buttonStateChanged15(pin):
    global pins
    global rooms
    global states
    global stdscr
    global offsetX
    global offsetY
    global writeDb

    time.sleep(.1)
    state = GPIO.input(pin)
    i = pins.index(pin)
    if state is not states[i]:
        states[i] = state
        ftime = datetime.now()
        ftime = ftime.strftime("%Y-%m-%d %H:%M:%S")
        status = state
        if (0 == state):
            state = 'Closed'
            attr = curses.color_pair(2)
        else:
            state = ' OPEN '
            attr = curses.color_pair(1) | curses.A_BOLD
        stdscr.addstr(i + offsetY, 20 + offsetX, state, attr)
        stdscr.addstr(i + offsetY, 30 + offsetX, ftime)
        stdscr.refresh()

        if True == writeDb:
            doUpdateDb = updateDb(i, status, ftime)
            doUpdateDb.start()

        doBeep = sensorBeep(state)
        doBeep.start()

######################################################
# Pin 16
######################################################

def buttonStateChanged16(pin):
    global pins
    global rooms
    global states
    global stdscr
    global offsetX
    global offsetY
    global writeDb

    time.sleep(.1)
    state = GPIO.input(pin)
    i = pins.index(pin)
    if state is not states[i]:
        states[i] = state
        ftime = datetime.now()
        ftime = ftime.strftime("%Y-%m-%d %H:%M:%S")
        status = state
        if (0 == state):
            state = 'Closed'
            attr = curses.color_pair(2)
        else:
            state = ' OPEN '
            attr = curses.color_pair(1) | curses.A_BOLD
        stdscr.addstr(i + offsetY, 20 + offsetX, state, attr)
        stdscr.addstr(i + offsetY, 30 + offsetX, ftime)
        stdscr.refresh()

        if True == writeDb:
            doUpdateDb = updateDb(i, status, ftime)
            doUpdateDb.start()

        doBeep = sensorBeep(state)
        doBeep.start()

######################################################
# Pin 17
######################################################

def buttonStateChanged17(pin):
    global pins
    global rooms
    global states
    global stdscr
    global offsetX
    global offsetY
    global writeDb

    time.sleep(.1)
    state = GPIO.input(pin)
    i = pins.index(pin)
    if state is not states[i]:
        states[i] = state
        ftime = datetime.now()
        ftime = ftime.strftime("%Y-%m-%d %H:%M:%S")
        status = state
        if (0 == state):
            state = 'Closed'
            attr = curses.color_pair(2)
        else:
            state = ' OPEN '
            attr = curses.color_pair(1) | curses.A_BOLD
        stdscr.addstr(i + offsetY, 20 + offsetX, state, attr)
        stdscr.addstr(i + offsetY, 30 + offsetX, ftime)
        stdscr.refresh()

        if True == writeDb:
            doUpdateDb = updateDb(i, status, ftime)
            doUpdateDb.start()

        doBeep = sensorBeep(state)
        doBeep.start()

######################################################
# Pin 18
######################################################

def buttonStateChanged18(pin):
    global pins
    global rooms
    global states
    global stdscr
    global offsetX
    global offsetY
    global writeDb

    time.sleep(.1)
    state = GPIO.input(pin)
    i = pins.index(pin)
    if state is not states[i]:
        states[i] = state
        ftime = datetime.now()
        ftime = ftime.strftime("%Y-%m-%d %H:%M:%S")
        status = state
        if (0 == state):
            state = 'Closed'
            attr = curses.color_pair(2)
        else:
            state = ' OPEN '
            attr = curses.color_pair(1) | curses.A_BOLD
        stdscr.addstr(i + offsetY, 20 + offsetX, state, attr)
        stdscr.addstr(i + offsetY, 30 + offsetX, ftime)
        stdscr.refresh()

        if True == writeDb:
            doUpdateDb = updateDb(i, status, ftime)
            doUpdateDb.start()

        doBeep = sensorBeep(state)
        doBeep.start()

######################################################
# Initialize all the global arrays and set up the
# GPIO as inputs, with edge detection.
######################################################


def initialize():
    global rids
    global pins
    global rooms
    global states
    global stdscr
    global writeDb
    global bounceTime

    # Read the configuration to see if we are updating the database
    with open('./config.json', 'r') as f:
        config = json.load(f)

    if 'true' == config['enable']:
        writeDb = True
    else:
        writeDb = False

    # Get the debounce time
    bounceTime = int(config['bounceTime'])

    # Get the room/pin info from the database
    roomdata = getrooms()

    # Set up the global arrays
    for rid, roomname, pin in roomdata:
        rids.append(rid)
        pins.append(pin)
        rooms.append(roomname)
        states.append(None)

    # Set up the GPIO
    setupGPIO()

    # Initialize the curses screen display
    stdscr = curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    # Initialize the screen with the room numbers and states
    initializeDisplay()


######################################################
# Initialize the monitor all the doors
# The only way out of this is by pressing CTRL + C
######################################################


def monitorDoors():
    global dbLock
    global beepLock
    global writeDb

    # Initialize the door sensors
    initialize()

    if True == writeDb:
        dbLock = threading.Lock()

    beepLock = threading.Lock()

    try:

        # Loop forever, but sleep to reduce CPU usage
        while True:
            time.sleep(5)

    except KeyboardInterrupt:
        # Caught CTRL + C
        # Clean up GPIO and reset the screen
        GPIO.cleanup()
        curses.endwin()
        print("Exiting program")
