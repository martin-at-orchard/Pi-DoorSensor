#!/usr/bin/python3
#
# Monitor door magnetic switches for opening and closing
#
# Author:  Martin Wedepohl <martin@orchardrecovery.com>
#
# Date:    October 15, 2020 - 0.1 - Original Issue
#
# Version: 0.1

######################################################
# Module Imports
######################################################
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
