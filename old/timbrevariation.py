
import numpy,math,random
from scipy.io.wavfile import write

#notes=[('c',32.7),('c#',34.65),('d',36.71),('d#',38.89),('e',41.2),('f',43.65),
#    ('f#',46.25),('g',49),('g#',51.91),('a',55),('a#',58.27),('b',61.47)]
notes={'c':32.7032,'c#':34.6478,'db':34.6478,'d':36.7081,'d#':38.8909,'eb':38.8909,'e':41.2034,'e#':43.6535,'fb':41.2034,'f':43.6535,'f#':46.2493,
   'gb':46.2493,'g':48.9994,'g#':51.9131,'ab':51.9131,'a':55.0,'a#':58.2705,'bb':58.2705,'b':61.7354,'b#':32.7032,'cb':61.73542,'r':0}


noteTypes={'q':1,'dq':1.5,'h':2,'dh':3,'w':4,'e':.5,'de':.75,'tr':1/3,'t':1/3,'s':.25,'ds':.375,'th':.125,'2t':2/3,
    'q,t':4/3,'h,t':7/3,'dh,t':10/3,'h,2t':8/3,'e,t':.5+1/3,'e,2t':.5+2/3,'tw':1/6,'sx':1/6,'q,2t':1+2/3,
    }

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
        x=(math.sin(incadd)+.3162*math.sin(2*incadd+3)+.15*math.sin(3*incadd+6)+.3162*math.sin(4*incadd)+.12*math.sin(5*incadd)+.3*math.sin(6*incadd+3)+.08*math.sin(7*incadd)+.15*math.sin(8*incadd)+.05*math.sin(9*incadd)+.01*math.sin(10*incadd))
        bytelist.append(amp*int(round(math.e**(-(2*i)/(samplerate*time))*(2**(bitspersample - 1) - 1)*x)))
        incadd += increment
    return bytelist


def noteToNum(s):
    beatLen=1/(tempo/60)
    l=s.split()
    freq=notes[l[0]]
    octave=int(l[1])-1
    value=noteTypes[l[2]]
    if len(l)<4:
        a=amp
    else:
        a=int(l[3])
    nums=(freq*2**octave,value*beatLen,a)
    return nums

last=None
last2=None

def songToWave(song):
    result=[]
    voices=[]
    global last,last2,tempo,amp
    for voice in song:
        tempo=tempo0
        amp=amp0
        print('v',voice)
        voiceWave=[]
        for chord in voice:
            print('c',chord)
            chordWave=[]
            if isinstance(chord,int):
                tempo=chord
                continue
            elif isinstance(chord,float):
                amp=chord
                continue
            elif isinstance(chord,str):
                if chord=='re':
                    voiceWave+= last
                    continue
                elif chord=='re2':
                    voiceWave+=last2
                    continue
                (f,t,a)=noteToNum(chord)
                chordWave=numpy.array(make_wave(f,t,a))
            else:
                for note in chord:
                    (f,t,a)=noteToNum(note)
                    tone=numpy.array(make_wave(f,t,a))
                    if chordWave==[]:
                        chordWave=tone
                    else:
                        chordWave+=tone
            
            chordWave=numpy.ndarray.tolist(chordWave)
            last2=last
            last=chordWave
            voiceWave+=chordWave
        print(len(voiceWave))
        finalVoice=numpy.array(voiceWave)
        voices.append(finalVoice)
    lengths=map(len,voices)
    shortest=min(lengths)
    for voice in voices:
        voice=voice[:shortest]
        if result==[]:
            result=voice
        else:
            result+=voice
    return numpy.ndarray.tolist(result)

# to add note
# data+=make_wave(freq,time)
def play(song,name):
    song=songToWave(song)
    scaled = numpy.int16(song/numpy.max(numpy.abs(song)) * 32767)
    print(scaled)
    write('%s.wav'%name, 44100, scaled)

tempo0=50
tempo=50 #bpm
tempo1=60
tempo2=80

amp0=100.0
amp=100
amp1=70.0
amp2=50.0

#play([['a 4 w']],'test')

clairDeLune=[
# Soprano voice
[
'r 4 2t','ab 5 q,t','f 5 q,t',
'eb 5 t','f 5 t','eb 5 h,t',
'db 5 t','eb 5 t','db 5 e','f 5 q','db 5 e,t',
'c 5 t','db 5 t','c 5 h,t',
'bb 4 t','c 5 t','bb 4 t','eb 5 t','bb 4 t','ab 4 t','bb 4 t','ab 4 2t',
'gb 4 t','ab 4 t','gb 4 q','f 4 q,t',
'f 4 t','gb 4 t','f 4 t','bb 4 t','f 4 t','eb 4 t','f 4 t','eb 4 2t',
'db 4 t','eb 4 t','db 4 q','c 4 q',

'r 4 t','ab 3 t','r 4 t','ab 5 q','f 5 q,t',
'eb 5 t','f 5 t','eb 5 h,t',
('db 4 t','db 5 t'),('eb 4 t','eb 5 t'),('ab 4 q','ab 5 q'),('f 4 q,t','f 5 q,t'),
'eb 5 t','f 5 t','eb 5 q','db 5 q,t',
('db 4 t 105','db 5 t 105'),('eb 4 t 120','eb 5 t 120'),('bb 4 e 160','bb 5 e 160'),('ab 4 q 150','ab 5 q 150'),('f 4 e,t 150','f 5 e,t 150'),
'eb 5 t 140','f 5 t 150','eb 5 e 130','db 5 q 120','bb 4 e 100',

# Tempo rubato
tempo1,
'r 4 e',('f 5 e,t','bb 5 e,t','f 6 e,t'),('eb 5 t','bb 5 t','eb 6 t'),'re','re',('db 5 t','bb 5 t','db 6 t'),'re',
're',('c 5 t','gb 5 t','bb 5 t','c 6 t'),'re',('c 5 e','gb 5 e','bb 5 e','c 6 e'),('db 5 e','bb 5 e','db 6 e'),('bb 4 q','gb 5 q','bb 5 q'),
'r 4 e',('f 5 e,t','bb 5 e,t','f 6 e,t'),('gb 5 t','bb 5 t','gb 6 t'),('f 5 t','bb 5 t','f 6 t'),('eb 5 t','bb 5 t','eb 6 t'),'re2','re',
('db 5 t','bb 5 t','db 6 t'),('eb 5 t','bb 5 t','eb 6 t'),'re2',('bb 5 e','c 6 e'),('db 5 e','bb 5 e','db 6 e'),('bb 4 dq','gb 5 dq','bb 5 dq'),

('gb 4 e','gb 5 e'),('ab 4 e','eb 5 e','ab 5 e'),('c 5 e','c 6 e'),('bb 4 e','gb 5 e','bb 5 e'),('gb 4 e','gb 5 e'),
'r 4 t',('gb 4 t','c 5 t','eb 5 t','gb 5 t'),'re','re','re',('ab 4 t','c 5 t','eb 5 t','ab 5 t'),('gb 4 q','c 5 q','eb 5 q','gb 5 q'),
'r 4 e',('gb 4 e','gb 5 e'),('ab 4 e','ab 5 e'),('db 5 e','db 6 e'),('bb 4 e','bb 5 e'),('gb 4 e','gb 5 e'),
'r 4 t',('gb 4 t','bb 4 t','eb 5 t','gb 5 t'),'re','re','re',('ab 4 t','c 5 t','f 5 t','ab 5 t'),('gb 4 q','bb 4 q','eb 5 q','gb 5 q'),
'r 4 e',('gb 4 e','gb 5 e'),('ab 4 e','ab 5 e'),('eb 5 e','eb 6 e'),('db 5 e','db 6 e'),('bb 4 e','bb 5 e'),
'r 4 t',('bb 4 t','eb 5 t','bb 5 t'),'re','re','re',('c 5 t','ab 5 t','c 6 t'),'re2',('db 5 t','bb 5 t','db 6 t'),('eb 5 t','bb 5 t','eb 6 t'),
('ab 5 h','db 6 h','ab 6 h'),('ab 5 q 80','db 6 q 80','ab 6 q 80'),
('ab 5 h 60','db 6 h 60','ab 6 h 60'),('ab 4 h 40','eb 5 h 40','ab 5 h 40'),
# Un poco mosso (tempo change)
tempo2,
'ab 4 h','cb 4 2t','db 5 t',
'ab 4 h','cb 4 2t','ab 4 t',
'db 5 2t','eb 5 t','f 5 q','db 5 2t','f 5 t',
'g 5 t','f 5 t','db 5 t',('db 5 q','bb 4 q'),'r 4 q',
'bb 4 h','c 5 2t','f 5 t',
'bb 4 h','c 5 2t','f 5 t',
'gb 5 dq','f 5 e','d 5 e','eb 5 e',
'bb 5 h','ab 5 q',
'ab 5 h','cb 5 2t','db 6 t',
'ab 5 h','b 5 2t','g# 5 t',

# En animant
'c# 6 q','e 6 q','g# 6 q',
'g# 6 q','f# 6 h',
'f# 6 h','a 6 2t','c# 7 t',
'f# 5 h','a 5 2t','c# 6 t',
'e 6 t','d# 6 t','c# 6 t','b 5 e','a 5 e,t','g# 5 t','f# 5 t',
'e 5 t','d# 5 t','c# 5 t','b 4 t 95','a 4 t 90','g# 4 2t 85','f# 4 t 80','e 4 t 75',
# Calmato
amp1,
('db 4 h','eb 4 h'),('eb 4 2t','gb 4 2t'),('eb 4 t','gb 4 t','bb 4 t'),
('db 4 h','eb 4 h'),('eb 4 2t','gb 4 2t'),('eb 4 t','gb 4 t','bb 4 t'),
('db 4 t','gb 4 t','bb 4 t'),('ab 4 t','c 5 t','f 5 t'),('gb 4 t','bb 4 t','eb 5 t'),('gb 4 q','bb 4 q'),('gb 4 q','ab 4 q'),
('db 4 t','gb 4 t','bb 4 t'),('ab 4 t','c 5 t','f 5 t'),('gb 4 t','bb 4 t','eb 5 t'),('gb 4 q','bb 4 q'),('gb 4 q','ab 4 q'),
'eb 5 h','gb 5 2t','bb 5 t',
'eb 5 h','gb 5 2t','bb 5 t',
'eb 6 w',
70,'db 6 q 65',60,'eb 6 q 55',

# a Tempo
tempo0,
amp2,
'r 4 q','ab 6 q','f 6 q,t',
'eb 6 t','f 6 t','eb 6 h,t',
'db 6 t','eb 6 t','db 6 e','f 6 q','db 6 e,t',
'c 6 t','db 6 t','c 6 h',
'r 4 t','bb 5 t','c 6 t','bb 5 t','eb 6 t','bb 5 t','ab 5 t','bb 5 t','ab 5 2t',
'gb 5 t','ab 5 t','gb 5 q','f 5 q,t',
'f 5 t','gb 5 t','f 5 t','bb 5 t','f 5 t','eb 5 t','f 5 t','eb 5 2t',
'db 5 t','eb 5 t','db 5 q','c 5 q',
'r 4 q',('f 5 q','ab 5 q'),('db 5 q,t','f 5 q,t'),
'eb 5 t','f 5 t','eb 5 h,t',
('db 4 t','db 5 t'),('eb 4 t','eb 5 t'),'ab 5 q','f 5 q,t',
'eb 5 t','f 5 t','eb 5 q','db 5 q',
'r 4 t','db 4 t','eb 4 t','bb 4 q','f 4 q',
tempo0-5,
'r 4 t','gb 4 t','ab 4 t','db 5 q','bb 4 q',
tempo0-10,
'r 4 t','bb 4 t','c 5 t','f 5 q','ab 4 q',

# morendo
tempo1,
'r 4 dh',
'r 4 q',tempo1-3,amp2-8,'cb 4 q','db 5 q',
'r 4 dh',
'r 4 q',tempo1-6,amp2-12,'cb 5 q','db 6 q',
tempo1-10,amp2-15,'cb 5 q','db 6 q',tempo1-15,amp2-20,'fb 6 q',
'ab 6 dh',
amp2-40,
('ab 5 dh','db 6 dh','f 6 dh','ab 6 dh'),
],
# Alto voice
[
'r 4 2t','f 5 q,t','db 5 q,t',
'c 5 t','db 5 t','c 5 h,t',
'bb 4 t','c 5 t','bb 4 h,t',
'ab 4 t','bb 4 t','ab 4 h',
'gb 4 h','gb 4 q',
'eb 4 h','eb 4 q',
'db 4 dh',
'bb 3 h','ab 3 q',

'r 4 t','ab 3 t','r 4 t','f 5 q','db 5 q,t',
('gb 4 h,2t','bb 4 h,2t'),
'r 4 t','ab 4 2t','ab 4 q','db 5 q',
'r 4 t',('gb 4 h,2t','bb 4 h,2t'),
'r 4 t','ab 4 2t 140','f 5 h 140',
'r 4 t',('f 4 h,2t 120','bb 4 h,2t 120'),

# Tempo rubato
tempo1,
'r 4 dh',
're',
're',
're',
're',
're',
'r 4 e','db 5 q','r 4 e','gb 5 q',
'r 4 dh',
'r 4 e',('bb 4 q','db 5 q'),'r 4 e',('gb 5 q','bb 5 q'),
'r 4 dh',
're',
'r 4 w',
# Un poco mosso
tempo2,
'f 4 h','ab 4 q',
'f 4 h','ab 4 2t','r 4 t',
'f 4 2t','ab 4 t','db 5 q','f 4 2t','db 5 t',
'eb 5 t','db 5 t','bb 4 t','g 4 t','f 4 t','db 4 t','db 4 e','bb 4 e',
'r 4 h','r 4 2t','ab 4 sx','f 4 sx',
'r 4 h','r 4 2t','ab 4 sx','f 4 sx',
'r 4 q','r 4 sx','gb 4 sx','bb 4 sx','f 5 sx','gb 4 sx','bb 4 sx','d 4 sx','gb 4 sx','bb 4 sx','eb 5 sx','gb 4 sx','bb 4 sx',
'r 4 dh',
'f 5 h','ab 5 2t','r 4 t',
'f 5 h','g# 5 2t','r 4 t',

# En animant
'r 4 e','c# 5 sx','g# 5 sx','e 5 sx','r 4 e','e 5 sx','c# 6 sx','g# 5 sx','r 4 e','g# 5 sx','e 6 sx','b 5 sx',
'r 4 dh',
'r 4 dh',
'r 4 dh',
'c# 6 t','b 5 t','a 5 t','g# 5 e','f# 5 e,t','e 5 t','d# 5 t',
'c# 5 t','b 4 t','a 4 t','g# 4 t 95','f# 4 t 90','e 4 2t 85','d# 4 t 80','c# 4 t 75',
# Calmato
amp1,
'gb 3 2t','ab 3 t','bb 3 2t','db 4 t','c 4 q',
'gb 3 2t','ab 3 t','bb 3 2t','db 4 t','c 4 q',
'r 4 q','db 4 t','bb 3 t','db 4 t','bb 3 t','c 4 t','eb 4 t',
'r 4 q','db 4 t','bb 3 t','db 4 t','bb 3 t','c 4 t','eb 4 t',
'r 4 sx','eb 4 sx','gb 4 sx','bb 4 sx','gb 4 sx','eb 4 sx','r 4 sx','eb 4 sx','gb 4 sx','bb 4 sx','gb 4 sx','eb 4 sx','r 4 q',
'r 4 sx','eb 4 sx','gb 4 sx','bb 4 sx','gb 4 sx','eb 4 sx','r 4 sx','eb 4 sx','gb 4 sx','bb 4 sx','gb 4 sx','eb 4 sx','r 4 q',
'r 3 dh',
'r 3 q',70,'r 3 q',60,'r 3 q',

# a Tempo
tempo0,
amp2,
'r 4 q','f 6 q','r 4 q',
'r 4 t','c 6 t','db 6 t','c 6 h,t',
'bb 5 t','c 6 t','bb 5 e','db 6 q','bb 5 e,t',
'ab 5 t','bb 5 t','ab 5 h',
'r 4 t','gb 5 t','ab 5 t','gb 5 q','f 5 q,t',
'eb 5 t','f 5 t','eb 5 q','a 4 q',
'r 4 t','db 5 t','eb 5 t','db 5 q','db 5 q',
'r 4 t','bb 4 t','c 5 t','bb 4 q','ab 4 q',
'r 4 t',('f 3 t','ab 3 t'),('f 4 h,t','ab 4 h,t'),
'r 4 t',('gb 4 h,2t','bb 4 h,2t'),
'r 4 t','ab 4 2t',('db 4 q','f 4 q','ab 4 q','f 5 q'),('db 4 q','f 4 q','db 5 q'),
'r 4 t',('f 4 h,2t','bb 4 h,2t'),
'r 4 t','ab 3 2t',('db 4 q','f 4 q'),('ab 3 q','db 4 q'),
tempo0-5,
'r 4 t',('bb 3 2t','db 4 2t'),('gb 4 q','bb 4 q'),('db 4 q','gb 4 q'),
tempo0-10,
'r 4 t',('c 4 2t','gb 4 2t'),('ab 4 q','c 5 q'),('c 4 q','gb 4 q'),

# morendo
tempo1,
'r 4 dh',
'r 4 q',tempo1-3,amp2-8,'ab 4 q','fb 4 q',
'r 4 dh',
'r 4 q',tempo1-6,amp2-12,'ab 5 h',
tempo1-10,amp2-15,'ab 5 h',tempo1-15,amp2-20,'r 4 q',
'f 6 dh',
'r 4 dh',
],
# Tenor voice
[
'r 4 t','ab 4 h,2t',
'a 4 dh',
'ab 4 dh',
'gb 4 dh',
'eb 4 h','eb 4 q',
'db 4 h','c 4 q',
'bb 3 dh',
'ab 3 h','gb 3 q',

'db 2 2t','ab 4 h,t',
'r 4 t',('db 3 h,2t','gb 3 h,2t','bb 3 h,2t','db 4 h,2t'),
'r 4 t',('f 3 2t','ab 3 2t'),('db 4 q','f 4 q'),('ab 3 q','db 3 q'),
'r 4 t',('db 3 h,2t','gb 3 h,2t','bb 3 h,2t','db 4 h,2t'),
'r 4 t',('f 3 2t 120','cb 3 2t 120'),('cb 3 q,t 140','db 4 q,t 140','f 4 q,t 160'),'r 4 2t',
'r 4 t',('f 3 e,2t 120','bb 3 e,2t 120','eb 4 e,2t 120'),'db 4 dq 110',

# Tempo rubato
tempo1,
'r 4 e',('f 4 e,t','gb 4 e,t','bb 4 e,t'),('eb 4 t','gb 4 t','bb 4 t'),'re','re',('db 4 t','gb 4 t','bb 4 t'),'re',
're',('c 4 t','gb 4 t','bb 4 t'),'re',('c 4 e','gb 4 e','bb 4 e'),('db 4 e','gb 4 e','bb 4 e'),('bb 3 q','db 4 q','gb 4 q'),
'r 4 e',('f 4 e,t','gb 4 e,t','bb 4 e,t'),('gb 4 t','bb 4 t','eb 5 t'),('f 4 t','gb 4 t','bb 4 t'),('eb 4 t','gb 4 t','bb 4 t'),'re2','re',
('db 4 t','gb 4 t','bb 4 t'),('eb 4 t','gb 4 t','bb 4 t'),'re2',('c 4 e','gb 4 e','bb 4 e'),('db 4 e','gb 4 e','bb 4 e'),('bb 3 q','eb 4 q','gb 4 q'),

'r 4 e','gb 3 e','ab 3 e','c 4 e','bb 3 e','gb 3 e',
'r 4 t',('gb 3 t','c 4 t','eb 4 t'),'re','re','re',('ab 3 t','c 4 t','eb 4 t'),('gb 3 q','c 4 q','eb 4 q'),
'r 4 e','gb 3 e','ab 3 e','db 4 e','bb 3 e','gb 3 e',
'r 4 t',('gb 3 t','bb 3 t','eb 4 t'),'re','re','re',('ab 3 t','c 4 t','f 4 t'),('gb 3 q','bb 3 q','eb 4 q'),
'r 4 e','gb 3 e','ab 3 e','eb 4 e','db 4 e','bb 3 e',
'r 4 t',('bb 3 t','db 4 t','gb 4 t'),'re','re','re',('c 4 t','eb 4 t','ab 4 t'),'re2',('db 4 t','gb 4 t','bb 4 t'),('eb 4 t','gb 4 t',' bb 4 t'),
('f 4 h','ab 4 h','db 5 h','f 5 h'),('fb 4 q 80','ab 4 q 80','bb 4 q 80','db 5 q 80','fb 5 q 80'),
('eb 4 h 60','gb 4 h 60','ab 4 h 60','db 5 h 60','eb 5 h 60'),('ab 3 h 40','eb 4 h 40','gb 4 h 40','c 5 h 40'),
# Un poco mosso
tempo2,
'db 2 sx','ab 2 sx','db 3 sx','f 3 sx','ab 3 sx','db 4 sx','f 2 sx','c 3 sx','f 3 sx','ab 3 sx','c 4 sx','f 4 sx','ab 2 sx','fb 3 sx','ab 3 sx','cb 3 sx','fb 4 sx','ab 4 sx',
'db 2 sx','ab 2 sx','db 3 sx','f 3 sx','ab 3 sx','db 4 sx','f 2 sx','c 3 sx','f 3 sx','ab 3 sx','c 4 sx','f 4 sx','ab 2 sx','fb 3 sx','ab 3 sx','cb 3 sx','ab 4 sx','fb 4 sx',
'db 2 sx','ab 2 sx','db 3 sx','f 3 sx','ab 3 sx','db 4 sx','f 4 sx','ab 4 sx','f 4 sx','db 4 sx','ab 3 sx','f 3 sx','ab 3 sx','f 3 sx','db 3 sx','ab 2 sx','db 3 sx','ab 2 sx',
'eb 2 sx','bb 2 sx','eb 3 sx','g 3 sx','bb 3 sx','eb 4 sx','g 4 sx','eb 4 sx','bb 3 sx','g 3 sx','eb 3 sx','bb 2 sx','eb 2 sx','bb 2 sx','eb 3 sx','g 3 sx','eb 3 sx','bb 2 sx',
'ab 2 sx','eb 3 sx','gb 3 sx','bb 3 sx','c 4 sx','gb 4 sx','gb 2 sx','db 3 sx','gb 3 sx','bb 3 sx','db 4 sx','gb 4 sx','f 2 sx','c 3 sx','f 3 sx','ab 3 sx','c 4 t',
'ab 2 sx','eb 3 sx','gb 3 sx','bb 3 sx','c 4 sx','gb 4 sx','gb 2 sx','db 3 sx','gb 3 sx','bb 3 sx','db 4 sx','gb 4 sx','f 2 sx','c 3 sx','f 3 sx','ab 3 sx','c 4 t',
'eb 2 sx','bb 2 sx','eb 3 sx','gb 3 sx','bb 3 sx','eb 4 sx','gb 4 e','f 4 e','d 4 e','eb 4 e',
'd 4 sx','gb 4 sx','bb 4 sx','bb 4 sx','gb 5 sx','bb 5 sx','eb 4 sx','gb 4 sx','bb 4 sx','bb 4 sx','gb 5 sx','bb 5 sx','c 4 sx','e 4 sx','ab 4 sx','c 5 sx','e 5 sx','ab 5 sx',
'db 3 sx','ab 3 sx','db 4 sx','f 4 sx','ab 4 sx','db 5 sx','ab 3 sx','c 4 sx','f 4 sx','ab 4 sx','c 5 sx','f 5 sx','cb 3 sx','fb 4 sx','ab 4 sx','cb 4 sx','fb 5 sx','ab 5 sx',
'db 3 sx','ab 3 sx','db 4 sx','f 4 sx','ab 4 sx','db 5 sx','ab 3 sx','c 4 sx','f 4 sx','ab 4 sx','c 5 sx','f 5 sx','cb 3 sx','fb 4 sx','ab 4 sx','cb 4 sx','g# 5 sx','e 5 sx',

# En animant
'c# 4 sx','e 4 sx','g# 4 sx','b 4 e','e 4 sx','g# 4 sx','b 4 sx','c# 5 e','g# 4 sx','b 4 sx','c# 5 sx','e 5 e',
'g# 4 sx','a 4 sx','c# 5 sx','g# 5 sx','c# 6 sx','a 5 sx','f# 4 sx','a 4 sx','c# 5 sx','f# 5 sx','c# 6 sx','a 5 sx','f# 4 sx','a 4 sx','c# 5 sx','f# 5 sx','c# 6 sx','a 5 sx',
'f# 4 sx','a 4 sx','c# 5 sx','f# 5 sx','c# 6 sx','a 5 sx','f# 4 sx','a 4 sx','c# 5 sx','f# 5 sx','c# 6 sx','a 5 sx','e 4 sx','a 4 sx','c# 5 sx','e 5 sx','c# 7 sx','c# 6 sx',
'b 3 sx','d# 4 sx','f# 4 sx','f# 4 sx','c# 5 sx','a 4 sx','a 3 sx','c# 4 sx','e 4 sx','f# 4 sx','c# 5 sx','a 4 sx','g# 3 sx','c# 4 sx','e 4 sx','a 4 sx','e 5 sx','a 5 sx',
'f# 3 sx','c# 4 sx','e 4 sx','f# 4 sx','a 4 sx','c# 5 sx','e 5 sx','f# 5 sx','e 5 sx','c# 5 sx','a 4 sx','f# 4 sx','e 4 sx','f# 4 sx','e 4 sx','c# 4 sx','a 3 sx','f# 3 sx',
'f# 2 sx','c# 3 sx','e 3 sx','f# 3 sx','a 3 sx','c# 4 sx 97','e 4 sx 93','c# 4 sx 90','a 3 sx 87','f# 3 sx 82','e 3 sx 78','c# 3 sx 73','f# 2 sx 70','c# 3 sx 70','re2','re','re2','re',
# Calmato
amp1,
'ab 2 sx','eb 3 sx','re2','re','re2','re','re2','re','re2','re','re2','re','re2','re','re2','re','re2','re',
're2','re','re2','re','re2','re','re2','re','re2','re','re2','re','re2','re','re2','re','re2','re',
'ab 2 sx','eb 2 sx','ab 2 sx','eb 3 sx','ab 2 sx','eb 3 sx','ab 3 sx','eb 3 sx','ab 3 sx','eb 4 sx','ab 3 sx','eb 3 sx','ab 3 sx','eb 3 sx','ab 2 sx','eb 3 sx','ab 2 sx','eb 2 sx',
'ab 2 sx','eb 2 sx','ab 2 sx','eb 3 sx','ab 2 sx','eb 3 sx','ab 3 sx','eb 3 sx','ab 3 sx','eb 4 sx','ab 3 sx','eb 3 sx','ab 3 sx','eb 3 sx','re2','re','re2','re',
'db 4 h','c 4 sx','eb 4 sx','gb 4 sx','bb 4 sx','c 5 sx','eb 5 sx',
'db 4 h','c 4 sx','eb 4 sx','gb 4 sx','bb 4 sx','c 5 sx','eb 5 sx',
'gb 4 sx','bb 4 sx','db 5 sx','eb 5 sx','gb 5 sx','bb 5 sx','gb 4 sx','bb 4 sx','db 5 sx','eb 5 sx','gb 5 sx','c 6 sx','gb 4 sx','bb 4 sx','db 5 sx','eb 5 sx','gb 5 sx','bb 5 sx',
'gb 4 sx','a 4 sx','db 5 sx','eb 5 sx','gb 5 sx','a 5 sx',70,'gb 4 sx','a 4 sx 68','db 5 sx 66','eb 5 sx 64','gb 5 sx 62','cb 5 sx 60',60,'gb 4 sx 58','a 4 sx 56','db 5 sx 54','eb 5 sx 52','gb 5 sx 50','a 5 sx 50',

# a Tempo
tempo0,
amp2-10.0,
'f 4 sx','ab 4 sx','c 5 sx','f 5 sx','ab 5 sx','c 6 sx','r 4 h',
'f 4 sx','a 4 sx','c 5 sx','eb 5 sx','f 5 sx','a 5 sx','r 4 h',
'f 4 sx','ab 4 sx','bb 4 sx','db 5 sx','f 5 sx','ab 5 sx','r 4 h',
'eb 4 sx','gb 4 sx','ab 4 sx','c 5 sx','eb 5 sx','gb 5 sx','r 4 h',
'db 4 sx','eb 4 sx','gb 4 sx','bb 4 sx','db 5 sx','eb 5 sx','r 4 q',('eb 4 q','f 4 q','ab 4 q','c 5 q'),
'c 3 sx','gb 3 sx','bb 3 sx','c 4 sx','eb 4 sx','gb 4 sx','bb 4 q',('c 4 q','eb 4 q'),
'ab 3 sx','bb 3 sx','db 4 sx','f 4 sx','ab 4 sx','bb 4 sx','r 4 q',('bb 3 q','db 4 q','eb 4 q'),
'f 3 sx','ab 3 sx','bb 3 sx','db 4 sx','f 4 sx','ab 4 sx','r 4 q',('gb 3 q','c 4 q'),
'ab 2 q','r 4 h',
'r 4 t',('db 3 h,2t','gb 3 h,2t','bb 3 h,2t','db 4 h,2t'),
'r 4 t',('f 3 2t','ab 3 2t'),'cb 3 h',
'r 4 t',('f 3 q,2t','bb 3 q,2t','eb 4 q,2t'),'db 4 q',
'r 4 dh',
tempo0-5,
'r 4 q','eb 3 q','eb 4 q',
tempo0-10,
'ab 2 e','eb 3 e','ab 5 q','ab 3 q',

# morendo
tempo1,
'db 2 sx','ab 2 sx','db 3 sx','f 3 sx','ab 3 sx','db 4 sx','f 2 sx','c 3 sx','f 3 sx','ab 3 sx','c 4 sx','f 4 sx','db 2 sx','ab 2 sx','db 3 sx','f 3 sx','ab 3 sx','db 4 sx',
'f 2 sx','c 3 sx','f 3 sx','ab 3 sx','c 4 sx','f 4 sx',tempo1-3,amp2-13,'ab 2 sx','fb 3 sx','ab 3 sx','cb 3 sx','fb 4 sx','gb 4 sx','ab 4 q',
'db 3 sx','ab 3 sx','db 4 sx','f 4 sx','ab 4 sx','db 5 sx','f 3 sx','c 4 sx','f 4 sx','ab 4 sx','c 5 sx','f 5 sx','db 3 sx','ab 3 sx','db 4 sx','f 4 sx','ab 4 sx','db 5 sx',
'f 3 sx','c 4 sx','f 4 sx','ab 4 sx','c 5 sx','f 5 sx',tempo1-6,amp2-16,'ab 3 sx','cb 3 sx','fb 4 sx','ab 4 sx','cb 4 sx','fb 5 q','r 4 sx',
tempo1-10,amp2-20,'ab 3 sx','cb 3 sx','fb 4 sx','ab 4 sx','cb 4 sx','fb 5 q','r 4 sx',tempo1-15,amp2-18,'r 4 q',
'db 2 sx','ab 2 sx','db 3 sx','f 3 sx','ab 3 sx','db 4 sx',amp2-22,'f 4 t','ab 4 t','db 5 t','f 5 t',amp2-25,'ab 5 t','db 6 t',
'r 4 dh',
],
# Bass voice
[
'r 4 t ','f 4 h,2t',
'gb 4 dh',
'f 4 dh',
'eb 4 dh',
'db 4 h','c 4 q',
'bb 3 h','a 3 q',
'ab 3 h','gb 3 q',
'f 3 h','eb 3 e','ab 2 e,t',

'r 4 tr','f 4 h,t',
('gb 2 dh 110','db 3 dh 110'),
('f 2 dh 110','db 3 dh 110'),
('gb 2 dh 120','db 3 dh 120'),
'ab 2 dh 140',
'bb 2 dh 120',

# Tempo rubato
tempo1,
('eb 1 dh','eb 2 dh'),
'r 4 dh',
('eb 1 dh','db 2 dh','bb 2 dh'),
'r 4 dh',

('ab 1 dh','ab 2 dh'),
('a 1 dh','a 2 dh'),
('bb 1 dh','bb 2 dh'),
('c 2 dh','c 3 dh'),
('db 2 dh','db 3 dh'),
('eb 2 dh','eb 3 dh'),
'r 4 dh',
'r 4 w',

# Un poco mosso
tempo2,
'db 2 q','f 2 q','ab 2 q',
'db 2 q','f 2 q','ab 2 q',
'r 4 dh',
'r 4 dh',
'ab 2 q','gb 2 q','f 2 q',
'ab 2 q','gb 2 q','f 2 q',
'eb 2 q','r 4 h',
'db 4 q','eb 4 q','ab 3 q',
'db 3 q','f 3 q','ab 3 q',
'db 3 q','f 3 q','g# 3 q',

# En animant
'b 3 q','c# 4 q','e 4 q',
'g# 4 q','f# 4 q','e# 4 q',
'e 4 q','d# 4 q','c# 4 q',
'b 3 q','a 3 q','g# 3 q',
'f# 3 dh',
'r 4 dh',
# Calmato
amp1,
'r 4 dh',
're',
're',
're',
'gb 3 2t','ab 3 t','bb 3 2t','db 4 t','c 4 q',
'gb 3 2t','ab 3 t','bb 3 2t','db 4 t','c 4 q',
'gb 4 dh',
'gb 4 q',70,'r 4 q',60,'gb 4 q 60',

# a Tempo
tempo0,
amp2-10.0,
'f 4 h','f 4 q',
'f 4 h','f 4 q',
'f 4 h','f 4 q',
'eb 4 h','eb 4 q',
'db 4 h','c 4 q',
'c 3 h','f 3 q',
'ab 3 h','bb 3 q',
'f 3 h','eb 3 e','ab 2 e',
'db 2 q','cb 3 h',
('gb 2 dh','db 3 dh'),
'ab 2 dh',
'bb 2 dh',
'f 2 dh',
tempo0-5,
'eb 2 dh',
tempo0-10,
'ab 2 dh',

# morendo
tempo1,
'db 2 q','f 2 q','db 2 q',
'f 2 q',tempo1-3,amp2-13,'ab 2 h',
'db 3 q','f 3 q','db 3 q',
'f 3 q',tempo1-6,amp2-16,'ab 3 h',
tempo1-10,amp2-20,'ab 3 h',tempo1-15,amp2-20,'ab 2 q',
'db 2 dh',
amp2-40,
('db 4 dh','ab 4 dh','db 5 dh','f 5 dh'),
]]



play(clairDeLune,'clair de lune')