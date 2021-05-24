#!/usr/bin/python3

###########################################################
#
# Imports
#
###########################################################

import json
import mariadb
import sys

###########################################################
#
# Function imports
#
###########################################################

from threading import Thread

###########################################################
#
# Database class
#
# Used to handle all the database interactions
#
###########################################################

class DB(Thread):

    #######################################################
    #
    # Class initialization
    #
    # Reads the database configuration, makes a test
    # connection to the database and then exits.
    #
    # @param: self This object
    #
    #######################################################

    def __init__(self):
        Thread.__init__(self)

        self.enableresults = False
        self.user =  ''
        self.password = ''
        self.host = ''
        self.database = ''

        # Get the connection
        try:
           with open('./config.json', 'r') as f:
               config = json.load(f)

               if 'enableresults' in config:
                   if 'true' == config['enableresults']:
                       self.enableresults = True

               self.user = config['user']
               self.password = config['password']
               self.host = config['host']
               self.database = config['database']

               conn = self.getConnection()
               conn.close()

        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Database: {e}")
            sys.exit(1)

    #######################################################
    #
    # Get all the room name, pins and id from the database.
    #
    #######################################################

    def getConnection(self):
        try:
            conn = mariadb.connect(
                user = self.user,
                password = self.password,
                host = self.host,
                database = self.database
            )

            return conn

        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Database: {e}")
            sys.exit(1)

    #######################################################
    #
    # Get all the room name, pins and id from the database.
    #
    #######################################################

    def getRooms(self):
        conn = self.getConnection()
        cur = conn.cursor()

        # Get the rooms/pins information
        enabled = 1
        cur.execute("SELECT r.id AS rid, r.name AS roomname, g.pin FROM rooms r INNER JOIN gpio g ON r.gpio=g.id WHERE enabled=? ORDER BY displayorder", (enabled,))

        data = []
        for rid, roomname, pin in cur:
            data += [[rid, roomname, pin]]

        conn.close()

        return data

    #######################################################
    #
    # Update results in database only if the enableresults
    # flag has been set
    #
    #######################################################

    def updateResults(self, room, status, date):
        if False == self.enableresults:
            return

        try:
            conn = self.getConnection()
            cur = conn.cursor(prepared=True)

            sql = "INSERT INTO results (room, status, date) VALUES(%d, %d, %s)"
            values = (room, status, date.strftime("%Y-%m-%d %H:%M:%S"))

            cur.execute(sql, values)
            conn.commit()

        except Error as e:
            # Ignore the error for now
            pass

        finally:
            conn.close()
