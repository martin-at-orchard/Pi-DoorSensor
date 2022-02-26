#!/usr/bin/python3

#######################################################
#
# Function to handle updating the screen
#
# Author: Martin Wedepohl <martin@orchardrecovery.com>
#
#######################################################

#######################################################
#
# Module Imports
#
#######################################################
import curses

#######################################################
#
# Function Imports
#
#######################################################
from datetime import datetime
from threading import Thread

#######################################################
#
# Class to display and update the display
#
#######################################################
class Display(Thread):

    ###################################################
    #
    # Initialize the class
    #
    # This class uses the curses library to perform simple
    # screen updates.
    #
    # Open doors are flagged as white on red
    # Closed doors are flagged as green on black
    #
    # @param self      The current object
    # @param offsetX   The screen offset in the X direction
    # @param offsetY   The screen offset in the Y direction
    # @param closedStr The string for a closed door
    # @param openStr   The string for an opened door
    #
    ###################################################
    def __init__(self, offsetX, offsetY, closedStr, openStr):
        Thread.__init__(self)
        self.stdscr = curses.initscr()
        self.offsetX = offsetX
        self.offsetY = offsetY
        self.doorOffsetX = offsetX + 0
        self.stateOffsetX = offsetX + 15
        self.timeOffsetX = offsetX + 25
        self.closedStr = closedStr
        self.openStr = openStr
        self.displayOrder = None
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    ###################################################
    #
    # Get the attribute based on the door state
    #
    # @param self  The current object
    # @param state The state of the door
    #
    # @return attr The screen attributes
    #
    ###################################################
    def getAttr(self, state):
        if self.openStr == state:
            attr = curses.color_pair(1) | curses.A_BOLD
        else:
            attr = curses.color_pair(2)

        return attr

    ###################################################
    #
    # Setup the screen
    #
    # @param self        The current object
    # @param displayData The Room data to display
    #
    ###################################################
    def setup(self, displayData):
        num = 0
        maxGpio = 28
        self.displayOrder = [0] * (maxGpio + 1)
        for rid, roomname, pinVal in displayData:
            now = datetime.now()
            nowStr = now.strftime("%c")
            state = self.openStr
            if 0 == pinVal:
                state = self.closedStr
            attr = self.getAttr(state)

            num = num + 1
            self.displayOrder[rid] = num

            self.stdscr.addstr(self.displayOrder[rid] + self.offsetY, self.doorOffsetX, roomname)
            self.stdscr.addstr(self.displayOrder[rid] + self.offsetY, self.stateOffsetX, state, attr)
            self.stdscr.addstr(self.displayOrder[rid] + self.offsetY, self.timeOffsetX, nowStr)

        self.stdscr.refresh()

    ###################################################
    #
    # Update the screen
    #
    # @param self       The current object
    # @param door       The door
    # @param pinVal     The value of the GPIO pin value
    # @param changeTime The time of the door change
    #
    ###################################################
    def update(self, door, pinVal, changeTime):
        state = self.openStr
        if 0 == pinVal:
            state = self.closedStr
        attr = self.getAttr(state)
        self.stdscr.addstr(self.displayOrder[door] + self.offsetY, self.stateOffsetX, state, attr)
        self.stdscr.addstr(self.displayOrder[door] + self.offsetY, self.timeOffsetX, changeTime)
        self.stdscr.refresh()

    ###################################################
    #
    # Cleanup the screen
    #
    # @param self The current object
    #
    ###################################################
    def cleanup(self):
        curses.endwin()
