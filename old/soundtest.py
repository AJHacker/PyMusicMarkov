import pysynth
import scipy.io
import numpy

test=(('c',1),('c',1))
test1=(('f',1),('g',1))
pysynth.make_wav(test,fn='test.wav')
pysynth.make_wav(test,fn='test1.wav')

data=scipy.io.wavfile.read('test.wav')
data1=scipy.io.wavfile.read('test1.wav')
final=[]
for i in range(len(data[1])):
    final.append(data[1][i]+data1[1][i])

scipy.io.wavfile.write('final.wav',44100,final)
