#!/usr/bin/python3
#
# Database calls to handle the rooms.
#
# Author:  Martin Wedepohl <martin@orchardrecovery.com>
#
# Date:    October 15, 2020 - 0.1 - Original Issue
#
# Version: 0.1

######################################################
# Module Imports
######################################################
import mariadb
import json
import sys

######################################################
# Connect to the database
######################################################


def getConnection():
    # Connect in a try block
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)

        conn = mariadb.connect(
            user=config['user'],
            password=config['password'],
            host=config['host'],
            database=config['database']
        )
        return conn

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Database: {e}")
        sys.exit(1)

######################################################
# Call to the database to get the listing of rooms
# and GPIO numbers
######################################################


def getrooms():
    # Connect in a try block
    try:

        conn = getConnection()
        cur = conn.cursor()

        # Get the rooms information
        enabled = 1
        cur.execute("SELECT r.id AS rid, r.name AS roomname, g.name AS gpioname FROM rooms r INNER JOIN gpio g ON r.gpio=g.id WHERE enabled=? ORDER BY displayorder", (enabled,))

        data = []
        for rid, roomname, gpioname in cur:
            data += [[rid, roomname, gpioname]]

        conn.close()

        return data

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Database: {e}")
        sys.exit(1)

######################################################
# Call to the database to get the listing of rooms
# and GPIO pins
######################################################


def getpins():
    # Connect in a try block
    try:

        conn = getConnection()
        cur = conn.cursor()

        # Get the rooms/pins information
        enabled = 1
        cur.execute("SELECT r.name AS roomname, g.pin FROM rooms r INNER JOIN gpio g ON r.gpio=g.id WHERE enabled=? ORDER BY displayorder", (enabled,))

        data = []
        for roomname, pin in cur:
            data += [[roomname, pin]]

        conn.close()

        return data

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Database: {e}")
        sys.exit(1)
