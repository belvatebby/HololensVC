'''
This program is supposed to identify the location of the speaker and 
calculate the distance of the speaker relative to one reference
created 20/03/2018
'''

#import pyaudio
import glob
import numpy as np
import wave
import math
import pika
import os
import pika

#CHUNK = 2**10 #chunk of data
#RATE = 16000 #sampling frequency


"""
list_of_files = glob.glob('D:\.TUGAS AKHIR\FTP-Folder\.wav') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
print latest_file

p = pyaudio.PyAudio()
stream=p.open(format=pyaudio.paInt16,
              channels=1,
              rate=RATE,
              input=True,
              frames_per_buffer=CHUNK)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='hello')
"""

directory = 'D:\.TUGAS AKHIR\FTP-Folder\localization'; #Path to the target file
#directory = 'D:\.TUGAS AKHIR\FTP-Folder'; #Path to the target file

RECORD_SECONDS = 1
#CHUNK = 1024
jarak = 0
fname1 = directory + '/RODE/dataRODE3m.0001.wav'
fname2 = directory + '/LOGITECH/dataMIC3m.0001.wav'
gain = 10

def sound_loc() :
    wav_file1 = wave.open(fname1, 'r')
    wav_file2 = wave.open(fname2, 'r')
    
    print(fname1)
    print(fname2)
	
    frate1 = wav_file1.getframerate()
    print(frate1)
    frate2 = wav_file2.getframerate()
    print(frate2)
	
	# Initial value
    peak1 = 0 
    peak1A = 0
    peak2 = 0
    peak2B = 0 
    L1 = 0
    L2 = 0
	
	#get data and peak for every sample iteration
    for i in range(int(frate2 / 1024 * RECORD_SECONDS)):
        data1 = np.fromstring(wav_file1.readframes(1024), dtype = np.int16)
        data2 = np.fromstring(wav_file2.readframes(1024), dtype = np.int16)
        peak1A = np.average(np.abs(data1))*2
        peak2B = np.average(np.abs(data2))*2
        #if peak1A>1000 and peak2B>1000 and peak1A < peak2B:
        if peak1A < peak2B:
            peak1 = peak1 + peak1A
            peak2 = peak2 + peak2B
        #if peak1A>1000 and peak2B>1000 and peak1A > peak2B:
            #peak1 = peak1
            #peak2 = peak2
        else :
            peak1 = peak1
            peak2 = peak2 + peak2B		
		#peak1 = peak1 + np.average(np.abs(data1))*2
        #peak2 = peak2 + np.average(np.abs(data2))*2
        print("RODE : %04f"%peak1)
        print("MIC : %04f"%peak2)
    
    print("peak sumber 1 = %04d"%peak1) #sumber 1 adalah mic Rode
    print("peak sumber 2 = %04d"%peak2) #sumber 2 adalah mic yang dipakai pengguna
    peak1_avg = (peak1 / (frate1 / 1024 * RECORD_SECONDS))
    peak2_avg = peak2 / (frate2 / 1024 * RECORD_SECONDS)	
    L1 = 20 * math.log10(peak1_avg/32767) #Intensitas suara dari perhitungan peak rata2 sumber 1
    print ("L1 = %03d"%L1)
    L2 = 20 * math.log10(peak2_avg/32767) #Intensitas suara dari perhitungan peak rata2 sumber 2
    print ("L2 = %03d"%L2)
    r2 = gain * (0.1 * 10**(np.abs(L1 - L2)/20))
    jarak = r2
    print("jarak pembicara adalah : %02f m"%jarak)
	#nChannels1 = wav_file1.getnchannels()
    #nChannels2 = wav_file2.getnchannels()

    #nSample1 = wav_file1.getsampwidth()
    #nSample2 = wav_file2.getsampwidth()	

    #data_size1 = data_size1 * nChannels1 * nSample1
    #data_size2 = data_size2 * nChannels2 * nSample2
     
    wav_file1.close()
    wav_file2.close()
    return jarak

sound_loc()
	
'''
sistem = True
stamp = "Null"
while (sistem==True):
    list_of_files = glob.glob('D:/.TUGAS AKHIR/FTP-Folder/*.txt') 
    list_of_files_wav = glob.glob('D:/.TUGAS AKHIR/FTP-Folder/*.wav') 
    latest_file = max(list_of_files, key = os.path.getmtime)
    if (stamp != latest_file):
        stamp = latest_file
        stamp_wav = max(list_of_files_wav, key = os.path.getmtime)
        #print (stamp)
        #checkfile = check(stamp)
        #print(checkfile)
        #while(checkfile == 0):
        #checkfile = check(stamp)
        #print(checkfile)
        sound_loc()	

'''
'''
def callback(ch, method, properties, body):
    

    #print(" [x] Received %r " %body)

channel.basic_consume(callback,
                      queue = 'hello',
                      no_ack = True)
			
print("[*] Waiting for message.")			
channel.start_consuming()
'''


