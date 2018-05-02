import os
import sys
from shutil import  copyfile
from time import gmtime, strftime 

timestamp = strftime("%d%m%y%H%M%S", gmtime())
src = 'D:\.TUGAS AKHIR\FTP-Folder\SoundA.wav'
dest = 'D:\.TUGAS AKHIR\FTP-Folder\LOG' + '/' + timestamp +'.wav'
copyfile(src, dest)

