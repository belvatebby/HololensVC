import pyaudio
import wave
import struct

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 2
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []
pointR = 0 
pointL = 0

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    count = len(data)/2
    format = "<%dh"%(count)
    x = struct.unpack(format,data)
    for i in range (len(x)-100):
	#for i in range(len(x)):
        if(x[i] > x[i+1]+40 and x[i] > x[i+2]+40 and x[i] > x[i+3]+40):
		    pointR += 1
        else:
		    pointL += 1

if(pointR < pointL):
    print ("left side")
else:
    print ("right side")

	
			
frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

