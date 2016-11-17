
import numpy,math,random,copy
from scipy.io.wavfile import write
from xmlParser import Parse
from numpy import linspace,sin,pi,int16

notes={
    'c':32.7032,
    'dbb':32.7032,
    'c#':34.6478,
    'db':34.6478,
    'c##':36.7081,
    'd':36.7081,
    'ebb':36.7081,
    'd#':38.8909,
    'eb':38.8909,
    'd##':41.2034,
    'e':41.2034,
    'e#':43.6535,
    'fb':41.2034,
    'e##':43.6535,
    'f':43.6535,
    'gbb':43.6535,
    'f#':46.2493,
    'gb':46.2493,
    'f##':48.9994,
    'g':48.9994,
    'abb':48.9994,
    'g#':51.9131,
    'ab':51.9131,
    'g##':55.0,
    'a':55.0,
    'bbb':55.0,
    'a#':58.2705,
    'bb':58.2705,
    'a##':61.7354,
    'b':61.7354,
    'b#':32.7032,
    'cb':61.73542/2,
    'r':0,
    'p':10,
   }

def memoized(f):
    # You are not responsible for how this decorator works
    # on the inside, just how to use it!
    import functools
    cachedResults = dict()
    @functools.wraps(f)
    def wrapper(*args):
        if args not in cachedResults:
            cachedResults[args] = f(*args)
        return cachedResults[args]
    return wrapper

@memoized
def make_wave(freq=440, time=1, amp=100, phase=0, samplerate=44100, bitspersample=16):
    bytelist = []
    k=2
    TwoPiDivSamplerate = 2*math.pi/samplerate
    if freq==10:
        (freq,k)=(70,8)
    if freq<71:
        amp=135
    elif freq<120:
        amp=120
    elif freq<110:
        amp=110
    amp/=100
    increment = TwoPiDivSamplerate * freq
    incadd = phase*increment
    for i in range(int(samplerate*time)):
        if incadd > (2**(bitspersample - 1) - 1):
            incadd = (2**(bitspersample - 1) - 1) - (incadd - (2**(bitspersample - 1) - 1))
        elif incadd < -(2**(bitspersample - 1) - 1):
            incadd = -(2**(bitspersample - 1) - 1) + (-(2**(bitspersample - 1) - 1) - incadd)
        #organ=(math.sin(incadd)+.3162*math.sin(2*incadd)+.15*math.sin(3*incadd)+.3162*math.sin(4*incadd)+.12*math.sin(5*incadd)+.3*math.sin(6*incadd)+.08*math.sin(7*incadd)+.15*math.sin(8*incadd)+.05*math.sin(9*incadd)+.01*math.sin(10*incadd))
        #whoop=math.e**(-((i-int(samplerate*time)/2)**2)/(2*(int(samplerate*time)/4)**2))*math.sin(incadd)
        #cello=math.sin(incadd)+.53*math.sin(2*incadd)+.375*math.sin(3*incadd)+.5*math.sin(4*incadd)+.375*math.sin(5*incadd)+.25*math.sin(6*incadd)+.23*math.sin(7*incadd)+.125*math.sin(8*incadd)+.16*math.sin(9*incadd)+.125*math.sin(10*incadd)+.125*math.sin(11*incadd)
        # x=cello
        # f=freq
        # if f!=0:
        #     while f<=10*freq:
        #         a=random.randint(1,5)/100
        #         x+=a*math.sin((f/freq)*incadd)
        #         f+=freq/10
        default=math.sin(incadd)
        bytelist.append(amp*int(round(math.e**(-(k*i)/(samplerate*time))*(2**(bitspersample - 1) - 1)*default)))
        incadd += increment
    return bytelist

# def make_wave(freq=440,time=1,amp=100,rate=44100):
#     t=linspace(0,time,time*rate)
#     data=sin(2*pi*freq*t)*amp

#     #instrument1=numpy.power(data,math.e**(-2*data/(time*rate)))

#     #instrument2
#     # def instrument2(x):
#     #     return math.e**((-2*x)/(rate*time))
#     # instrument2=numpy.vectorize(instrument2)
    
    
#     def f(x):
#         return math.e**((-5*x))*math.sin(2*pi*freq*x)*amp
#     f=numpy.vectorize(f)
#     data=f(t)
#     #data=instrument2(data)
#     return numpy.ndarray.tolist(data.astype(int16))

tempo=0 #bpm
tempo0=105

amp0=100.0
amp=100

def noteToNum(s):
    global lastOctave
    beatLen=1/(int(tempo)/60)
    l=s.split()
    freq=notes[l[0]]
    # if len(l)<3:
    #     octave=lastOctave
    # else:
    octave=int(l[1])-1
    #lastOctave=octave
    value=float(l[-1])
    if len(l)<4:
        a=amp
    else:
        a=int(l[3])
    nums=(freq*2**octave,value*beatLen,a)
    return nums

last=None
last2=None

def removeOutliers(L):
    if len(L)>2:
        lengths=list(map(len,L))
        lens=copy.deepcopy(lengths)
        med=median(lens)
        for voice in L:
            if abs(len(voice)-med)>med*.005:
                L.remove(voice)
        return L
    else:
        return L

def median(L):
    while len(L)>2:
        L.remove(max(L))
        L.remove(min(L))
    return L[0]

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
                tempo=tempoScale*chord
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
                        # chordWave+=tone
                        try:
                            chordWave+=tone[:len(chordWave)]
                        except:
                            tone=numpy.append(tone,[0]*(len(chordWave)-len(tone)))
                            chordWave+=tone
                            print('filled broken tie')
                            # print('Error occurred while creating chord')
                            # print('\n')
                            # return

            chordWave=numpy.ndarray.tolist(chordWave)
            last2=last
            last=chordWave
            voiceWave+=chordWave
        print(len(voiceWave))
        finalVoice=numpy.array(voiceWave)
        voices.append(finalVoice)

    voices=removeOutliers(voices)
    lengths=list(map(len,voices))
    med=median(lengths)
    for voice in voices:
        if len(voice)>=med:
            voice=voice[:med]
        else:
            voice=numpy.append(voice,[0]*(med-len(voice)))
        if result==[]:
            result=voice
        else:
            result+=voice
    return numpy.ndarray.tolist(result)

# to add note
# data+=make_wave(freq,time)
def play(parsedSong,filename):
    (song,tempo)=parsedSong
    global tempo0
    tempo0=tempoScale*tempo
    song=songToWave(song)
    scaled = numpy.int16(song/numpy.max(numpy.abs(song)) * 32767)
    print(scaled)
    try:
        write('%s.wav'%filename, 44100, scaled)
    except:
        print('fuck')
        write('%salt.wav'%filename, 44100, scaled)

tempoScale=1
 
play(Parse('pmat.xml'),'pmat')
#play(([['a 0 4']],60),'a')