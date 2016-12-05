import pygame
import subprocess
from pygame.locals import *
from xmlParser import Parse
import sys
from xml.dom import minidom
import os
from multiinstrument import playMarkov
import threading
import math
width = 300
height = 300
try:
    name = sys.argv[1]
    width = int(sys.argv[2])
    height = int(sys.argv[3])
except:
    name='uptown funk'
    width = 1280
    height = 800


notesDict = {
            'a':((255,0,0),0),
            'b':((0,255,0),2*math.pi/8),
            'c':((0,0,255),2*math.pi/4),
            'd':((255,69,0),2*3*math.pi/8),
            'e':((255,215,0),2*math.pi/2),
            'f':((138,43,226),2*5*math.pi/8),
            'g':((255,0,255),2*6*math.pi/8),
            'r':((176,196,222),2*7*math.pi/8),
            'p':((255,255,255),15*math.pi/8)}


class Voice(object):
    def __init__(self,data,voice):
        self.tempo = data.tempo
        self.voice = voice
        self.showed = 0
        self.x = data.width-data.width/3
        self.y = data.height/10 * (8-voice[0][2])-((ord(voice[0][1])-97)%97)*(data.width/10 /7)
    def move(self,canvas,data):
        for item in self.voice[:1]:
            appearAfter = item[0]
            if(appearAfter<data.pointInSong):
                self.x = data.width/2
                if(appearAfter<data.pointInSong):
                    note = item[1]
                    octave = item[2]
                    color = notesDict[note][0]
                    duration = item[3]
                    self.showed+=data.timerDelay
                    self.y = data.height/10 * (8-octave)-((ord(note)-97)%97)*(data.width/10 /7)
                    self.x = self.x - ((data.pointInSong-appearAfter) * data.tempo)
                    pygame.draw.circle(data.pygamecanvas,color,(int(self.x),int(self.y)),10)
                    #canvas.create_line(self.x+10,self.y+5,self.x-duration*self.tempo,self.y+5,width=2,fill=color)
                    if(self.showed>1/(2*self.tempo/duration/60)):
                        self.showed=0
                        self.voice.remove(item)
                    #if(data.pointInSong-appearAfter>10):
                    #    self.voice.remove(item)

def getBeatUnit(data,file):
    xmldoc=minidom.parse('XMLs/'+file+'.xml')
    try:beatUnit=beatUnits[part.getElementsByTagName('beat-unit')[0].childNodes[0].nodeValue]
    except:beatUnit=1
    return beatUnit

def mousePressed(data):pass

def keyPressed(data,event):
    if event.key==K_q:
        pygame.mixer.music.stop()
        pygame.quit()
        sys.exit()

def doPyGamestuff(fileName):
    class Struct(object):pass
    data=Struct()
    global width
    global height
    data.width=width
    data.height=height
    data.fileName = fileName
    pygame.init()
    flags=FULLSCREEN|DOUBLEBUF
    data.window=pygame.display.set_mode((data.width,data.height),flags)
    data.pygamecanvas = pygame.Surface((data.width,data.height))
    font = pygame.font.Font(None, 100)
    name = font.render(fileName.title(),1,(170,170,170))
    nw,nh=name.get_size()
    data.pygamecanvas.blit(name,(data.width/2-nw/2,data.height/2-nh/2))
    colors=(0,0,0)
    data.voices=[]
    data.pointInSong=0
    fpsClock=pygame.time.Clock()
    prepsong(data,data.fileName)
    fps=60
    data.timerDelay=1/fps
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN:
                keyPressed(data,event)
            elif event.type==MOUSEBUTTONDOWN:
                mousePressed(data)
        data.window.fill(colors)
        redrawAll(data)
        pygame.display.update()
        realfps=fpsClock.get_fps()
        try:
            data.timerDelay=1/realfps
        except:pass
        fpsClock.tick(fps)

def prepsong(data,file):
    data.songWithPositions = []
    song = Parse('XMLs/'+file+'.xml')
    data.beatUnit=getBeatUnit(data,file)
    pathtowav = 'WAV/'+file+'.wav'
    if not(os.path.isfile(pathtowav)):
        playMarkov(file,song[0],song[1])
    data.tempo = song[1]
    print(data.tempo)
    for voice in song[0]:
        pointInSong=0
        for note in voice:
            if(isinstance(note,str)):
                n = note.split(' ')
                note,octave,duration = n[0][0],int(n[1]),float(n[2])
                data.songWithPositions.append((pointInSong,note,octave,duration,data.tempo))
                pointInSong+=duration
            elif isinstance(note,tuple):
                n=note[0].split(' ')
                note,octave,duration = n[0][0],int(n[1]),float(n[2])
                data.songWithPositions.append((pointInSong,note,octave,duration,data.tempo))
                pointInSong+=duration
        data.voices.append(Voice(data,data.songWithPositions))
        data.songWithPositions = []

    print('done prepping')
    pygame.mixer.music.load(pathtowav)
    pygame.mixer.music.play(0,0.0)
    print('music should play')



def redrawAll(data):

    inc=(data.timerDelay)*(data.tempo/60)
    data.pointInSong +=inc
    data.pygamecanvas.fill((0,0,0))
    for i in range(8):
        pygame.draw.line(data.pygamecanvas,(170,170,170),(0,i*data.height/8+50),(data.width,i*data.height/8+50),3)
    for voice in data.voices:
        voice.move(data.pygamecanvas,data)

    data.pygamecanvas=data.pygamecanvas.convert()
    data.window.blit(data.pygamecanvas,(0,0))
    pass



if name != 'FUCK YOU':
    doPyGamestuff(name)
