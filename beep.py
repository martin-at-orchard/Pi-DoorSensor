#!/usr/bin/python3

import subprocess
from threading import Thread

###########################################################################
#
# Class to create a beep on a door open
#
###########################################################################
class Beep(Thread):

    #######################################################################
    #
    # Beeep class initialization
    #
    #######################################################################
    def __init__(self):
        Thread.__init__(self)

    def makeSound(self):
        p = subprocess.Popen([ 'mpg123', 'open_beep.mp3'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

