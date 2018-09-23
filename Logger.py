# logging times and names to a file for event parsing
import os
import time
from pathlib import Path
import csv
logPath = os.path.join(os.getcwd(), "face-log.txt")
FIELD_AMT = 2

class Logger(object):
    # initialization function that creates the log file
    def __init__(self):
        path = Path(logPath)
        if path.is_file():
            print("Found previous log file")
            file = open(logPath, "r")
            first_line = file.readline()
            if first_line is None or first_line == "":
                print("[1] File is empty")
                logFile = open(logPath, "w")
                logFile.write("Event Time\tIdentity\n")
            else:
                # checking if the header is correct
                logFile = open(logPath, "r")
                reader = csv.reader(logFile, delimiter='\t')
                row = next(reader)
                if len(row) > 1:
                    if row[0] == "Event Time" and row[1] == "Identity":
                        print("File correctly formatted")
                    else:
                        print("[1] File has an incorrectly formatted first line")
                        print("Please fix the headers and run again")
                else:
                    print("[2] File has an incorrectly formatted first line")
                    print("Please fix the headers and run again")
            # TODO: check if the data within the file is formatted correctly w/ FIELD_AMT
            # TODO: clean incorrectly formatted data
        else:
            print("No previous log file detected!")
            print("Creating new log file")
            # create new file w/ header
            logFile = open(logPath, "w")
            logFile.write("Event Time\tIdentity\n")
            logFile.close()

    def addLog(self, name, time):
            if time is None or name is None:
                print("[ERROR] no name or time to add to log file!")
            else:
                logFile = open(logPath, "a")
                logFile.write(time + "\t" + name + "\n")
                logFile.close()
                print("Added log")

    # parses through the log and returns time when person was last seen
    def checkLastSeen(self, name):
        logFile = open(logPath, "r")
        reader = csv.reader(logFile, delimiter='\t')
        lastSeen = ""
        for rows in reader:
            if rows[1] == name:
                lastSeen = rows[0]
        logFile.close()
        return lastSeen

# testing our new logger
logger = Logger()
time = str(int(time.time()))
logger.addLog("blake_edwards", time)
print("blake_edwards last seen @: " + logger.checkLastSeen("blake_edwards"))
