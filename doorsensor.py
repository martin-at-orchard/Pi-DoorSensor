#!/usr/bin/python3
#
# Monitor door magnetic switches for opening and closing
#
# Author:  Martin Wedepohl <martin@orchardrecovery.com>
#
# Date:     August  6, 2020 - 0.1 - Original Issue
#          October 15, 2020 - 0.2 - Loaded into VSC and linted
#         November 12, 2020 - 0.3 - pins.py and rooms.py update
#
# Version: 0.3

######################################################
# Module Imports
######################################################
#import mariadb
#import sys
from pins import monitorDoors

######################################################
# Main door sensor program
######################################################


def main():
    monitorDoors()

######################################################
# Main python program
######################################################


if __name__ == "__main__":
    main()
