
import numpy,math,random
from scipy.io.wavfile import write

#notes=[('c',32.7),('c#',34.65),('d',36.71),('d#',38.89),('e',41.2),('f',43.65),
#    ('f#',46.25),('g',49),('g#',51.91),('a',55),('a#',58.27),('b',61.47)]
notes={'c':32.7032,'c#':34.6478,'db':34.6478,'d':36.7081,'d#':38.8909,'eb':38.8909,'e':41.2034,'e#':43.6535,'fb':41.2034,'f':43.6535,'f#':46.2493,
   'gb':46.2493,'g':48.9994,'g#':51.9131,'ab':51.9131,'a':55.0,'a#':58.2705,'bb':58.2705,'b':61.7354,'b#':32.7032,'cb':61.73542,'r':0}
tempo=50 #bpm
beatLen=1/(tempo/60)
noteTypes={'q':1,'dq':1.5,'h':2,'dh':3,'w':4,'e':.5,'de':.75,'tr':.33333,'t':.33333,'s':.25,'ds':.375,'t':.125,
    'q,tr':1.33333,'h,tr':2.33333}

def make_wave(freq=440, time=1, amp=100, phase=0, samplerate=44100, bitspersample=16):
    bytelist = []
    TwoPiDivSamplerate = 2*math.pi/samplerate
    increment = TwoPiDivSamplerate * freq
    incadd = phase*increment
    for i in range(int(samplerate*time)):
        if incadd > (2**(bitspersample - 1) - 1):
            incadd = (2**(bitspersample - 1) - 1) - (incadd - (2**(bitspersample - 1) - 1))
        elif incadd < -(2**(bitspersample - 1) - 1):
            incadd = -(2**(bitspersample - 1) - 1) + (-(2**(bitspersample - 1) - 1) - incadd)
        bytelist.append(amp*int(round(math.e**(-(2*i)/(samplerate*time))*(2**(bitspersample - 1) - 1)*math.sin(incadd))))
        incadd += increment
    return bytelist

def noteToNum(s):
    #print(s)
    l=s.split()
    freq=notes[l[0]]
    octave=int(l[1])-1
    value=noteTypes[l[2]]
    if len(l)<4:
        amp=100
    else:
        amp=int(l[3])
    return (freq*2**octave,value*beatLen,amp)

def songToWave(song):
    result=[]
    for chord in song:
        chordWave=None
        if isinstance(chord,str):
            (f,t,a)=noteToNum(chord)
            chordWave=numpy.array(make_wave(f,t,a))
        else:
            for note in chord:
                (f,t,a)=noteToNum(note)
                tone=numpy.array(make_wave(f,t,a))
                if chordWave==None:
                    chordWave=tone
                else:
                    chordWave+=tone
        a=numpy.ndarray.tolist(chordWave)
        result+=a
    return result

# to add note
# data+=make_wave(freq,time)
def play(song):
    song=songToWave(song)
    scaled = numpy.int16(song/numpy.max(numpy.abs(song)) * 32767)
    print(scaled)
    write('test1.wav', 44100, scaled)

clairDeLune=[
'r 4 tr 0',('f 4 tr 30','ab 4 tr 30'),('f 5 q 60','ab 5 q 60'),
('db 5 q 50','f 5 q 50'),('gb 4 tr 30','ab 4 tr 30'),('c 5 tr 40','eb 5 tr 40'),
('db 5 tr 50','f 5 tr 50'),('c 5 h 40','eb 5 h 40'),('f 4 tr 30','ab 4 tr 30'),
('bb 4 tr 30','db 5 tr 30'),('c 5 tr 40','eb 5 tr 40'),('bb 4 e 30','db 5 e 30'),
'f 5 q 40','db 5 e 40',('eb 4 tr 30','gb 4 tr 30'),('ab 4 tr 40','c 5 tr 40'),
('bb 4 tr 40','db 5 tr 40'),('ab 4 h 40','c 5 h 40'),

('gb 4 tr 40','db 4 tr 30','eb 4 tr 40'),'bb 4 tr 35','c 5 tr 40','bb 4 tr 40','eb 5 tr 50','bb 4 tr 40',
('gb 4 tr 40','ab 4 tr 40','c 4 tr 30','eb 4 tr 30'),'bb 4 tr 45','ab 4 tr 40',
('eb 4 tr 30','bb 3 tr 30','db 4 tr 30'),
'gb 4 tr 40','ab 4 tr 45','gb 4 q 40',('eb 4 q 40','f 4 q 40','a 3 q 30','c 4 q 30'),
('db 4 tr 30','ab 3 tr 30','bb 3 tr 30'),'f 4 tr 40','gb 4 tr 40','f 4 tr 40','bb 4 tr 45','f 4 tr 40',
('eb 4 tr 40','gb 3 tr 30','bb 3 tr 30'),'f 4 tr 40','eb 4 tr 40',('bb 3 tr 35','f 3 tr 30','ab 3 tr 30'),
'db 4 tr 40','eb 4 tr 40','db 4 q 40',('ab 3 q 30','c 4 q 30'),

'ab 2 tr 20','db 2 tr 30',('f 3 tr 38','ab 3 tr 38'),('f 4 tr 45','ab 4 tr 45'),
('f 5 q 55','ab 5 q 55'),('db 5 q 45','f 5 q 45'),('gb 2 tr 30','db 3 tr 30'),
('db 3 tr 20','gb 3 tr 20','bb 3 tr 20','db 4 tr 20','gb 4 tr 40','bb 4 tr 40','eb 5 tr 50'),
'f 5 tr 40','eb 5 h 38',('f 2 tr 35','db 3 tr 35'),('f 3 tr 30','ab 3 tr 30','db 4 tr 40','ab 4 tr 35','db 5 tr 40'),
('eb 4 tr 50','eb 5 tr 50'),('db 3 q 65','f 3 q 65','db 4 q 70','ab 4 q 60','db 5 q 70'),
('ab 3 q 60','db 4 q 60','f 4 q 65','db 5 q 60','f 5 q 65'),
('gb 2 tr 60','db 3 tr 60'),('db 3 tr 50','gb 3 tr 50','bb 3 tr 50','db 4 tr 50',
'gb 4 tr 50','bb 4 tr 50','eb 5 tr 60'),'f 5 tr 65','eb 5 q 65','db 5 q 65',

'ab 3 tr 60',('f 3 tr 65','cb 3 tr 65','db 4 tr 70','ab 4 tr 65','db 5 tr 75'),
('eb 4 tr 75','eb 5 tr 85'),('c 4 e 70','db 4 e 70','f 4 e 70','bb 4 e 80','f 5 e 70','bb 5 e 100'),
('ab 4 q 80','ab 5 q 90'),('f 4 e 75','f 5 e 85'),'bb 2 tr 75',
('f 3 tr 65','bb 3 tr 65','eb 3 tr 65','f 4 tr 65','bb 4 tr 65','eb 5 tr 75'),
'f 5 tr 75','eb 5 e 65',('db 4 q 45','db 5 q 55'),'bb 4 e 45',
('eb 1 h 30','eb 2 h 40')]

play(clairDeLune)
print(notes['f']*2**4)