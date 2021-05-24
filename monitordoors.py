#!/usr/bin/python3
from threading import Thread
import queue
import json
from beep import Beep
import db

############################################################
#
# Class for the controller
#
###########################################################
class MonitorDoors(Thread):
    def __init__(self, inQueue, beepLock, display):
        self.inQueue = inQueue
        self.beepLock = beepLock
        self.display = display

    def run(self):
        beepTask = Beep()
        beepTask.run()
        while True:
            try:
                id, pinVal, now = self.inQueue.get()
                self.display.update(id, pinVal, now.strftime("%c"))

                if 1 == pinVal:
                    if False == self.beepLock.locked():
                        if True == self.beepLock.acquire(False):
                            beepTask.makeSound()
                            self.beepLock.release()

            except queue.Empty:
                continue

