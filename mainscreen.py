#Tkinter basic stuff, tried to implement some complex buttons and frames
#still working on it
# Barebones timer, mouse, and keyboard events
import subprocess
import multiprocessing
import datetime
from tkinter import *
from multiinstrument import playMarkov
import time
from visualizer import doPyGamestuff
import tkinter as tk
import signal
import math
import pygame
from pygame.locals import *
import threading
from markov import Markov
import os
from xml.dom import minidom
from xmlParser import Parse
import string
from webScraping import search,download
from init import init as initfilesystem
from queue import Queue
#from multiInstrument import play


notesDict = {
            'a':('red',0),
            'b':('green',2*math.pi/8),
            'c':('blue',2*math.pi/4),
            'd':('orange',2*3*math.pi/8),
            'e':('yellow',2*math.pi/2),
            'f':('purple',2*5*math.pi/8),
            'g':('pink',2*6*math.pi/8),
            'r':('grey',2*7*math.pi/8),
            'p':('white',15*math.pi/8)}

notesDict1 = {
            'a':('red',0),
            'b':('green',2*math.pi/8),
            'c':('blue',2*math.pi/4),
            'd':('orange',2*3*math.pi/8),
            'e':('yellow',2*math.pi/2),
            'f':('purple',2*5*math.pi/8),
            'g':('pink',2*6*math.pi/8),
            'r':('grey',2*7*math.pi/8),
            'p':('black',15*math.pi/8)}


class Voice(object):
    def __init__(self,data,voice):
        self.tempo = data.tempo
        self.voice = voice
        #self.showed = 5
        self.x = data.width-data.width/3
        self.y = data.height/10 * (8-voice[0][2])-((ord(voice[0][1])-97)%97)*(data.width/10 /7)
    def move(self,canvas,data):
        for item in self.voice[:1]:
            appearAfter = item[0]
            self.x = data.width-data.width/3
            if(appearAfter<data.pointInSong):
                note = item[1]
                octave = item[2]
                color = notesDict[note][0]
                duration = item[3]
                #self.showed+=1
                self.y = data.height/10 * (8-octave)-((ord(note)-97)%97)*(data.width/10 /7)

                canvas.create_oval(self.x-10,self.y-10,self.x+10,self.y+10,width=3,fill=color, outline=color)
                canvas.create_line(self.x+10,self.y+5,self.x-duration*self.tempo,self.y+5,width=2,fill=color)
                #if(self.showed>5):
                self.voice.remove(item)

class Button(object):
    def __eq__(self):
        pass

    def __init__(self,data,x1,y1,x2,y2,text,fill):
        self.x1,self.y1,self.x2,self.y2 = x1,y1,x2,y2
        self.text,self.fill = text,fill
        self.height = abs(y1-y2)
        self.width = abs(x1-x2)

    def checkBounds(self,x,y):
        if(x>self.x1 and y>self.y1 and x<self.x2 and y<self.y2):
            return True
        else:
            return False
        pass

    def draw(self,canvas,data):
        if(data.mousex>self.x1 and data.mousey>self.y1 and data.mousex<self.x2 and data.mousey<self.y2):
            canvas.create_rectangle(self.x1,self.y1,self.x2,self.y2,fill='light grey',width = 0)
        else:
            canvas.create_rectangle(self.x1,self.y1,self.x2,self.y2,fill=self.fill,width = 0)
        textScale = self.width*self.height//400
        canvas.create_text(self.x1+self.width/2,self.y1+self.width/6.5,text = self.text,font = 'Arial %d'%textScale)

def listFiles(path):
    if (os.path.isdir(path) == False):
        # base case:  not a folder, but a file, so return singleton list with its path
        return [path]
    else:
        # recursive case: it's a folder, return list of all paths
        files = [ ]
        for filename in os.listdir(path):
            files += listFiles(path + "/" + filename)
        return files

def doPyGamestuff(data):
    prepsong(data,data.filetovisualize)
    pygame.init()
    data.window=pygame.display.set_mode((data.width,data.height))
    data.pygamecanvas = pygame.Surface((data.width,data.height))
    colors=[(255,0,0),(0,255,0),(0,0,255)]
    i=0
    while True:
        fpsClock=pygame.time.Clock()
        data.window.fill(colors[i%3])
        i+=1
        pygame.display.update()
        fpsClock.tick(1)

####################################
# customize these functions
####################################

def init(data):
    data.pointInSong = 0
    data.fontScale = data.width*data.height // 20000
    data.margin = 10 #data.height/10
    data.boxwidth = data.width/10
    data.boxheight = data.height/10
    data.mainVisited = False
    data.screen = "HomeScreen"
    data.voices = []
    data.mousex,data.mousey = 0,0
    #tempo = 100
    #for x,y,t,z in [('a',4,.5,0),('b',4,.5,.5),('c',4,.5,1),('d',4,.5,1.5),('e',4,.5,2),('f',4,.5,2.5),('g',4,.5,3),('r',4,.5,3.5)]:
    #    data.dots.append(Circle(data,x,y,t,z,tempo))
    data.buttons = []
    b1 = Button(data,data.width/2-data.margin*10,data.height/2+data.margin*2,data.width/2+data.margin*10,data.height/2+data.margin*8,'Begin','red')
    data.buttons.append(b1)
    pass

def mousePressed(event, data):
    if(data.screen == "HomeScreen"):
        for button in data.buttons:
            if(button.checkBounds(event.x,event.y)):
                data.screen = "Main"
                data.buttons = []
        pass

def motion(event,data):
    data.mousex,data.mousey = event.x,event.y
 #  print(data.mousex,data.mousey)

def keyPressed(event, data):
    if(data.screen == "HomeScreen"):

        pass

q=Queue()
def timerFired(data):
    if(data.screen == 'Visualize'):
        inc=(data.timerDelay/1000)*(data.tempo/60)*data.beatUnit
        data.pointInSong +=inc
        #print(data.pointInSong)

    if(data.screen == "HomeScreen"):
        pass

def almostEqual(x,y):
    return abs(x-y)<10**(-3)

def playSong(pathtowav):
    subprocess.call(["afplay", pathtowav])

beatUnits={
    'quarter':1,
    'eighth':.5,
    'half':2,
}
def getBeatUnit(data,file):
    xmldoc=minidom.parse('XMLs/'+file+'.xml')
    try:beatUnit=beatUnits[part.getElementsByTagName('beat-unit')[0].childNodes[0].nodeValue]
    except:beatUnit=1
    return beatUnit


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


    t = threading.Thread(target=playSong,args=(pathtowav,))
    t.start()


def doCircleStuff(data,canvas):
    for button in data.buttons:
        button.draw(canvas,data)
    for voice in data.voices:
        voice.move(canvas,data)

def redrawAll(canvas, data):
    if(data.screen == 'Visualize'):
        canvas.create_rectangle(0,0,data.width,data.width,fill='black')
        canvas.create_text(data.width/2,data.height/2, anchor = S,text = data.filetovisualize,font = 'Arial %d bold'%data.fontScale)
        colors = ['red','orange','green','blue','purple','violet','red','orange','green','blue','purple','violet']
        for octave in range(8):
                #canvas.create_text(15+(linear*note)%2*30,linear*data.width/85,anchor = N,text = chr(note+65),font = 'Cochin 30',fill =colors[linear//7])

            canvas.create_line(15+octave*10,15+octave*data.width/15,data.width,15+octave*data.width/15,width = 1,fill='grey')

        canvas.create_line(0,15+octave*data.width/15,data.width,15+octave*data.width/15,width = 1,fill='grey')

        doCircleStuff(data,canvas)







    if(data.screen == "HomeScreen"):
        canvas.create_text(data.width/2,data.height/2, anchor = S,text = "Welcome to PyMarkovMusic",font = 'Arial %d bold'%data.fontScale)
        doCircleStuff(data,canvas)


    if(data.screen == "Main" and data.mainVisited == False):
        data.mainVisited = True
        data.dots = []
        data.pointInSong=0
        drawMainScreen(canvas,data)


    if(data.screen=='Main'):
        canvas.create_rectangle(0,0,data.width/3,data.height,fill='#85FF9E',width=0)
        Label(canvas,text='',bg = '#85FF9E').grid(row=1,column=0,sticky=N+W+E+S)

def drawMainScreen(canvas,data):
    initfilesystem()
    #results = [intVar()]*10
    #d = {0:None,1:None,2:None,3:None,4:None,5:None,6:None,7:None,8:None,9:None}
    for i in range(33):
        Label(canvas,text='',bg = '#473198').grid(row=i,column=2,sticky=N+W+E+S)
        Label(canvas,text='',bg = '#85FF9E').grid(row=i,column=0,sticky=N+W+E+S)
        Label(canvas,text='',bg = '#FFCECE').grid(row=i,column=1,sticky=N+W+E+S)


    data.checkbuttons = []
    data.buttonsdown = []
    data.xmlbuttons = []
    data.xmlbuttonsdown = []
    def getResults(query):
        data.searchresults = search(query)
        def create_checkbutton(name,views,increment):
            var = IntVar()

            cb = Checkbutton(canvas,bg = '#473198', text=name[:40]+'-'+views[:12],command=lambda:buttonsPushed(var))
            cb.grid(row=increment+2,column = 2,sticky=W)
            cb.var = var
            return cb
        data.checkbuttons = [create_checkbutton(name,views,increment) for increment,name,views,url,score in data.searchresults]
        #if(len(data.searchresults)<13):
        #    for i in range(len(data.searchresults),13):
        #        Label(canvas,text='',bg = '#473198').grid(row=i,column=2,sticky=N+W+E+S)

    def buttonsPushed(var):
        var = int(str(var).split('R')[-1])-len(data.xmlbuttons)
        #print(var)
        if(var in data.buttonsdown):
            data.buttonsdown.remove(var)
        else:
            data.buttonsdown.append(var)

    def getvals():
        for i in data.buttonsdown:
            download(data.searchresults[i][3],data.searchresults[i][1], data.searchresults[i][4])



    canvas.columnconfigure(0,minsize=data.width/3)
    #canvas.create_window(0,0,height=data.height,width=data.width/3,anchor = N+W)

    canvas.columnconfigure(1,minsize=data.width/3)
    canvas.columnconfigure(2,minsize=data.width/3)

    Label(canvas,text = "Search For Songs:",anchor = S,font = 'Arial 26 bold',bg = '#473198').grid(column = 2,row=0,sticky=W+E+N+S)
    Label(canvas, text="Saved XML Files:",anchor = S,font = 'Arial 26 bold',bg = '#85FF9E').grid(row=0,column = 0,sticky=W+E+N+S)

    tk.Button(canvas,text="Refresh",highlightbackground='#85FF9E',command = lambda:drawMainScreen(canvas,data)).grid(row = 0, column = 0, sticky = W)



    tk.Button(canvas,highlightbackground='#FFCECE',text="Generate Markov Music From XMLs",command=lambda:getxmls()).grid(row = 16, column = 1, sticky = N+S+E+W)
    e1 = Entry(canvas,width=33,highlightthickness=0)
    e1.grid(column=1,row=14,sticky=E,padx=30)
    Label(canvas,text="Filename:",bg='#FFCECE',anchor=S).grid(row=14,column=1,sticky=W,padx=30)


    tk.Button(canvas,text="Download All",command = lambda:getvals(),highlightbackground='#473198').grid(row = 13, column = 2, sticky = N+S+E+W)

    Label(canvas,bg='#473198').grid(column=2,row=1,sticky=N+W+E+S)
    e = Entry(canvas,width=25,highlightthickness=0)
    e.grid(column=2,row=1,sticky=W,padx=50)
    b = tk.Button(canvas,text="Search",command=lambda:getResults(e.get()),width=8,highlightbackground='#473198')
    b.grid(row = 1, column = 2, sticky = E,padx=50)

    files = open("data.txt", "r").readlines()
    data.files = [f.strip() for f in files]
    files = data.files

    def visualize(var):
        var = int(str(var).split('R')[-1])
        data.filetovisualize = data.files[var]
        #p = multiprocessing.Process(target=doPyGamestuff,args=(data,))
        #p.start()
        #doPyGamestuff(data,)
        subprocess.Popen(['python','/Users/Arihant/Desktop/PyMusicMarkov/visualizer.py', data.filetovisualize,str(data.width),str(data.height)])
        Label(canvas,text= 'PLEASE WAIT LOADING...',font = 'Arial 30 bold').grid(row=20,column=1,sticky=W)
    def makebutton(name,i):
        var = IntVar()
        cb = Checkbutton(canvas, text=name[:60],command=lambda:xmlchosen(var),bd=2,highlightthickness=0,bg='#85FF9E')
        cb.grid(row=i+2,column = 0, sticky=W)
        cb.var = var
        b1 = tk.Button(canvas,text='Visualize/Play',command=lambda:visualize(var),highlightbackground='#85FF9E')
        b1.grid(row=i+2,column=0,sticky=E)
        b1.var=var
        return cb

    data.xmlbuttons = [makebutton(data.files[i],i) for i in range(len(data.files))]
    def xmlchosen(var):
        var = int(str(var).split('R')[-1])-len(data.xmlbuttons)+1
        #print(var)
        if(var in data.xmlbuttonsdown):
            data.xmlbuttonsdown.remove(var)
        else:
            data.xmlbuttonsdown.append(var)

    def getxmls():

        xmlsToParse = []
        for i in data.xmlbuttonsdown:
            xmlsToParse.append('XMLs/'+files[i]+'.xml')
        if(xmlsToParse!=[]):
            print('Parsing:'+str(xmlsToParse)+'to:'+e1.get()+'.wav')
            l1 = Label(canvas,text = "Generating File - Please Wait",anchor = S,bg = '#FFFFFF')
            l1.grid(column=1,row=15,sticky=N+W+S+E)
            for f in xmlsToParse:
                temp = Markov(f)
            if(playMarkov('WAV/'+e1.get(),temp[0],temp[1])):
                l1 = Label(canvas,text = "File Created!",anchor = S,bg = '#FFFFFF')
                l1.grid(column=1,row=15,sticky=N+W+S+E)

        else:
            l1 = Label(canvas,text = "Please Select XMLs",anchor = S,bg = '#FFFFFF')
            l1.grid(column=1,row=15,sticky=N+W+S+E)
            #time.sleep(1.5)
            #l1.destroy()




####################################
# use the run function as-is
####################################
def redrawAllWrapper(canvas, data):
    canvas.delete(ALL)
    canvas.create_rectangle(0, 0, data.width, data.height,
                            fill='white', width=0)
    redrawAll(canvas, data)
    canvas.update()
def timerFiredWrapper(canvas, data):
    timerFired(data)
    redrawAllWrapper(canvas, data)
def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):

        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    root = Tk()
    data = Struct()
    data.timerDelay = 10 # milliseconds
    data.delay=20
    data.width = root.winfo_screenwidth()
    data.height = root.winfo_screenheight()
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    data.canvas = canvas

    init(data)

    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    root.bind('<Motion>', lambda event:motion(event,data))

    timerFiredWrapper(canvas, data)

    print('hello')
    # and launch the app
    root.mainloop()  # blocks until window is closed


    print("bye!")
    os.system('killall afplay')

run()
