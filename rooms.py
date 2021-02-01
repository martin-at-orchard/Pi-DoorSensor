#!/usr/bin/python3
#
# Database calls to handle the rooms.
#
# Author:  Martin Wedepohl <martin@orchardrecovery.com>
#
# Date:     August  6, 2020 - 0.1 - Original Issue
#          October 15, 2020 - 0.2 - Loaded into VSC and linted
#
# Version: 0.2

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
# and GPIO pins
######################################################


def getrooms():
    # Connect in a try block
    try:

        conn = getConnection()
        cur = conn.cursor()

        # Get the rooms/pins information
        enabled = 1
        cur.execute("SELECT r.id AS rid, r.name AS roomname, g.pin FROM rooms r INNER JOIN gpio g ON r.gpio=g.id WHERE enabled=? ORDER BY displayorder", (enabled,))

        data = []
        for rid, roomname, pin in cur:
            data += [[rid, roomname, pin]]

        conn.close()

        return data

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Database: {e}")
        sys.exit(1)

######################################################
# Update the results for later viewing
#
# @param int    room   The id of the room
# @param int    status The status of the room 0 = open, 1 = closed
# @param string date   The date/timestring of the change
#
# @return int Number of rows inserted
######################################################


def updateresults(room, status, date):
    # Connect in a try block
    try:

        conn = getConnection()
        cur = conn.cursor()

        sql = "INSERT INTO results (room, status, date) VALUES(%d, %d, %s)"
        data = (room, status, date)
        cur.execute(sql, data)
        conn.commit()
        numinserts = cur.rowcount

        conn.close()

        return numinserts

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Database: {e}")
        sys.exit(1)
