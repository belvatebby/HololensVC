#!/usr/bin/env python

import ftplib
import glob
import os
import sys
import time
import wave
from shutil import copyfile

def check(stamp):
    try:
        wave.open(stamp)
        return 1
    except wave.Error:
        print ("could not read")
        return 0

sistem = True
stamp = "Null"
#session = ftplib.FTP(host='192.168.88.22',user='FTP-User',passwd='hololens')
session = ftplib.FTP(host='192.168.88.22',user='voice',passwd='hololens')
while (sistem==True):
    list_of_files = glob.glob('/home/pi/Desktop/START/*.wav')
    latest_file = max(list_of_files, key=os.path.getmtime)
    if (stamp != latest_file):
        stamp = latest_file
        print (stamp)
        checkfile = check(stamp)
        print(checkfile)
        while(checkfile == 0):
            checkfile = check(stamp)
            print(checkfile)
        file = open(stamp,'rb')                  # file to send
        session.storbinary('STOR /data.0000.wav', file)     # send the file
        file.close()                                    # close file and FTP
        print (session.dir())
#print (session.retrlines('LIST'))
print (session.dir())
#session.mkd('voice')
#print (session.pwd())
#session.cwd(/voice)
#print (session.dir())
#print (session.dir())
session.quit()