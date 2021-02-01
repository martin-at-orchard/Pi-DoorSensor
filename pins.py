#!/usr/bin/python3
#
# Function to handle the door switches
#
# Author:  Martin Wedepohl <martin@orchardrecovery.com>
#
# Date:     August 26, 2020 - 0.1 - Original Issue
#          October 15, 2020 - 0.2 - Loaded into VSC and linted
#
# Version: 0.2
#
######################################################

######################################################
# Module Imports
######################################################
import RPi.GPIO as GPIO
import time
import curses
import os
import threading

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
times = []
states = []

debounce = 0.01
stdscr = None

dbLock = None
closedLock = None
openLock = None
inOpen = None
inClosed = None

######################################################
# Beep Threading class
######################################################


class sensorBeep(threading.Thread):
    def __init__(self, state):
        threading.Thread.__init__(self)
        self.state = state

    def run(self):
        global openLock
        global closedLock
        global inOpen
        global inClosed

        if ('Closed' == self.state):
            if (inClosed is None):
                inClosed = True
                closedLock.acquire()
                os.system('mpg123 -q close_beep.mp3')
                inClosed = None
                closedLock.release()
        else:
            if (inOpen is None):
                inOpen = True
                openLock.acquire()
                os.system('mpg123 -q open_beep.mp3')
                inOpen = None
                openLock.release()

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
    global times
    global states

    # We are using GPIO pin numbering
    GPIO.setmode(GPIO.BOARD)

    # Loop through all the pins
    # Set the time and read the current state of the switch
    numPins = len(pins)
    for i in range(numPins):
        GPIO.setup(pins[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        times[i] = datetime.now()
        states[i] = GPIO.input(pins[i])

######################################################
# Initialize the display with the rooms, times and initial states
######################################################


def initializeDisplay():
    global pins
    global rooms
    global times
    global states
    global stdscr

    numPins = len(pins)

    for i in range(numPins):
        room = rooms[i]
        ftime = times[i].strftime("%Y-%m-%d %H:%M:%S")
        if (0 == states[i]):
            state = 'Closed'
            attr = curses.color_pair(2)
        else:
            state = ' OPEN '
            attr = curses.color_pair(1) | curses.A_BOLD

        stdscr.addstr(i,  0, room)
        stdscr.addstr(i, 20, state, attr)
        stdscr.addstr(i, 30, ftime)

    stdscr.refresh()

######################################################
# Called when there is a change to the state of a GPIO input
# This uses curses to display the data on the screen
######################################################


def buttonStateChanged(pin):
    global pins
    global times
    global rooms
    global states
    global stdscr

    state = GPIO.input(pin)
    i = pins.index(pin)
    if state is not states[i]:
        elapsed = (datetime.now() - times[i]).total_seconds()
        if elapsed > debounce:
            states[i] = state
            times[i] = datetime.now()
            ftime = times[i].strftime("%Y-%m-%d %H:%M:%S")
            status = state
            if (0 == state):
                state = 'Closed'
                attr = curses.color_pair(2)
            else:
                state = ' OPEN '
                attr = curses.color_pair(1) | curses.A_BOLD
            stdscr.addstr(i, 20, state, attr)
            stdscr.addstr(i, 30, ftime)
            stdscr.refresh()
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
    global times
    global states
    global stdscr

    # Get the room/pin info from the database
    roomdata = getrooms()

    # Set up the global arrays
    for rid, roomname, pin in roomdata:
        rids.append(rid)
        pins.append(pin)
        rooms.append(roomname)
        times.append(None)
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

    # Set up the GPIO handler
    numPins = len(pins)
    for i in range(numPins):
        GPIO.add_event_detect(pins[i], GPIO.BOTH, callback=buttonStateChanged)

######################################################
# Initialize the monitor all the doors
# The only way out of this is by pressing CTRL + C
######################################################


def monitorDoors():
    global dbLock
    global closedLock
    global openLock

    # Initialize the door sensors
    initialize()

    dbLock = threading.Lock()
    closedLock = threading.Lock()
    openLock = threading.Lock()

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
