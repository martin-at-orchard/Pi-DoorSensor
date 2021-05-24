#!/usr/bin/python
from threading import Thread

############################################################
#
# Base class for a queue sender
#
###########################################################
class TXQueue(Thread):
    def __init__(self, name, txQueue, door):
        Thread.__init__(self)
        self.name = name
        self.txQueue = txQueue
        self.door = door
        self.start()

    def run(self):
        # no runner so far
        pass
