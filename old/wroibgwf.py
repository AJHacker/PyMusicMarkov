
import numpy,math,random
from scipy.io.wavfile import write

notes=[('c',32.7),('c#',34.65),('d',36.71),('d#',38.89),('e',41.2),('f',43.65),
    ('f#',46.25),('g',49),('g#',51.91),('a',55),('a#',58.27),('b',61.47)]
#notes={'c':32.7,'c#':34.65,'d':36.71,'d#':38.89,'e':41.2,'f':43.65,'f#':46.25,
 #   'g':49,'g#':51.91,'a':55,'a#':58.27,'b':61.47}
tempo=80
beatLen=1/(tempo/60)
noteTypes={'q':1,'h':2,'dh':3,'w':4,'e':.5,'s':.25,}
def damped_wave(frequency=440.0,time=2,samplerate=44100,amplitude=.5):
    points=make_wave(frequency,time)
    result=[]
    for i in range(len(points)):
        result.append(math.exp(-(float(i%time)/float(samplerate)))*points[i])
    return result

def make_wave(freq, time=1, amp=1, phase=0, samplerate=44100, bitspersample=16):
    bytelist = []
    TwoPiDivSamplerate = 2*math.pi/samplerate
    increment = TwoPiDivSamplerate * freq
    incadd = phase*increment
    for i in range(int(samplerate*time)):
        if incadd > (2**(bitspersample - 1) - 1):
            incadd = (2**(bitspersample - 1) - 1) - (incadd - (2**(bitspersample - 1) - 1))
        elif incadd < -(2**(bitspersample - 1) - 1):
            incadd = -(2**(bitspersample - 1) - 1) + (-(2**(bitspersample - 1) - 1) - incadd)
        bytelist.append(int(round(amp*(2**(bitspersample - 1) - 1)*math.sin(incadd))))
        incadd += increment
    return bytelist


starSpangledBanner=[
    ]
data = []
for octave in range(2,7):
    for note in notes:
        f=note[1]
        data+=damped_wave(f*2**octave,.3)





scaled = numpy.int16(data/numpy.max(numpy.abs(data)) * 32767)
print(scaled)
write('test.wav', 44100, scaled)
