'''
This program is supposed to identify the location of the speaker and 
calculate the distance of the speaker relative to one reference
created 20/03/2018
'''

import pyaudio
import numpy as np
import math
import pika

CHUNK = 2**10 #chunk of data
RATE = 16000 #sampling frequency


p = pyaudio.PyAudio()
stream=p.open(format=pyaudio.paInt16,
              channels=1,
              rate=RATE,
              input=True,
              frames_per_buffer=CHUNK)


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='hello')

j = 0
k = 0
sL1 = []
sum = 0
jarak = 0
def callback(ch, method, properties, body):
    L1 = float(body) #in dB
    #global sL2
    global j, sL1, sum, k, jarak
    print("%02d dBL1"%(L1))
    if (body != None) :
        L2 = 0 #in dB
        r1 = 0.1 #in meter
        r2 = 0 #in meter
        #sL1 = []
        sL1.append(L1)
        
		
        for i in range(int(1)): #go for a few seconds
            data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
            peak=np.average(np.abs(data))*2
            L2 = peak #L2 is compared to L1[i+1]
            print (L2)
            bars="#"*int(50*peak/2**16)
            print ("%04d %05d %s"%(i,peak,bars))
            L2 = 20 * math.log10(peak/32767)
            print ("%02d dBL2"%(L2))
            if (j>2) :
                r2 = 10*(r1 * 10**(np.abs(sL1[j-2] - L2)/20)) #calculate the distance of the speaker by comparing the intensity dB between it and reference
                print ("%05f dBcompared"%(sL1[j-2]))
                print ("%05f m"%(r2))
                if ((sL1[j-2]) > -20) :
                    sum = sum + r2
                    k = k+1
	
        j = j + 1
	
    if (j > 25) :
        jarak = sum/k
        print ("estimasi jarak = %04f"%(jarak))
        

    #print(" [x] Received %r " %body)

channel.basic_consume(callback,
                      queue = 'hello',
                      no_ack = True)
			
print("[*] Waiting for message.")			
channel.start_consuming()



stream.stop_stream()
stream.close()
p.terminate()

