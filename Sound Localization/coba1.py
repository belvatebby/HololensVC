import pyaudio
import wave
import struct
import urllib
#import pydub
import scipy.io.wavfile
import numpy as np
import math
from time import gmtime, strftime 

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 2
timestamp = strftime("%d%m%y%H%M%S", gmtime())
#k = 4

while True :
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    
    sistem = True
    while (sistem): #go for every seconds
        data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
        peak = np.average(np.abs(data))*2
        
        WAVE_OUTPUT_FILENAME = str(timestamp) +'.wav'
        #WAVE_OUTPUT_FILENAME = 'xxx.wav'
        sum = 0
        k = 0
        #bars="#"*int(50*peak/2**16)
        if peak > 1500:
            print("* recording")
            frames = []
            power = 0
            db = 0
            dbs = 0
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                sounddata = stream.read(CHUNK)
                data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
                peak = np.average(np.abs(data))*2
                bars="#"*int(50*peak/2**16)
                print ("%02d %05d %s"%(i,peak,bars))
                if (peak > 1500) :
                    print ("the peak is counted")
                    sum += peak
                    k += 1
				#data1 = stream.read(CHUNK)
                #x = np.fromstring(data1,dtype=np.int16)
                #db = np.sqrt((np.mean(np.abs(x))**2)) 	
                #dbs = dbs + (20*(math.log10(db)))
                #power = np.sum(np.abs(x)**2)
                frames.append(sounddata)
            avg = sum/k
            print ("the average is = %02f"%(avg))
			
			#poweravg = power / 31
            #dbsavg = dbs / 31
		    #x = np.array(data)
            #power = np.sum(np.data**2)
            stream.stop_stream()
            stream.close()
            p.terminate()
			
			
            #print("Intensity :")
            #print(poweravg)
            #print("dB :")
            #print(dbsavg)
			
			
            wf = wave.open(WAVE_OUTPUT_FILENAME , 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            sistem = False
            print("* done recording")
            #k = k + 1








