import glob
import os
from os import rename, listdir
import sys

sistem = True
stamp = "Null"
while (sistem == True):
    #list_of_files = glob.glob('C:\Users\user\Documents\Audacity') # * means all if need specific format then *.csv
    list_of_files = glob.glob('D:\.TUGAS AKHIR\FTP-Folder\*.wav') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key = os.path.getmtime)
    #print latest_file
    if (stamp != latest_file):
        #do something
        stamp = latest_file
        print ("file baru dibuat")


