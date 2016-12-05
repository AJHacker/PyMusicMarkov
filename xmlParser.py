##Algorithmic Help and Muic Theory Help and Code Help Credited to
##David Yang-dzy
##
##


from xml.dom import minidom
import string

keys={
    '0':set([]),
    # sharps
    '1':set(['f']),
    '2':set(['f','c']),
    '3':set(['f','c','g']),
    '4':set(['f','c','g','d']),
    '5':set(['f','c','g','d','a']),
    '6':set(['f','c','g','d','a','e']),
    '7':set(['f','c','g','d','a','e','b']),
    # flats
    '-1':set(['b']),
    '-2':set(['b','e']),
    '-3':set(['b','e','a']),
    '-4':set(['b','e','a','d']),
    '-5':set(['b','e','a','d','g']),
    '-6':set(['b','e','a','d','g','c']),
    '-7':set(['b','e','a','d','g','c','f']),

}

beatUnits={
    'quarter':1,
    'eighth':.5,
    'half':2,
}

beatTypes={
    '4':1,
    '8':.5,
    '2':2,
}

noteTypes={'q':1,'dq':1.5,'h':2,'dh':3,'w':4,'e':.5,'de':.75,'tr':1/3,'t':1/3,
    's':.25,'ds':.375,'th':.125,'2t':2/3,
    'q,t':4/3,'h,t':7/3,'dh,t':10/3,'h,2t':8/3,'e,t':.5+1/3,'e,2t':.5+2/3,
    'tw':1/6,'sx':1/6,'q,2t':1+2/3,'s,s':.5,'e,e':1,'q,e':1.5,'e,s':.625,'w,h':6,
    'e,th':.5+1/8,'q,th':1+1/8,'h,e':2.5,'h,s':2.25,'q,s':1.25,'dq,q':2.5,
    'dq,e':2,'dh,e':3.5,'dh,dq':4.5,'dq,s':1.75,'dh,q':4,'dq,dq':3,'dq,de':1.5+.75
    }

sharpOrder=[
    ('a',0),('a#',0),('b',0),
    ('c', 1), ('c#', 1), ('d', 1), ('d#', 1), ('e', 1), ('f', 1), ('f#', 1), ('g', 1), ('g#', 1), ('a', 1), ('a#', 1), ('b', 1),
    ('c', 2), ('c#', 2), ('d', 2), ('d#', 2), ('e', 2), ('f', 2), ('f#', 2), ('g', 2), ('g#', 2), ('a', 2), ('a#', 2), ('b', 2),
    ('c', 3), ('c#', 3), ('d', 3), ('d#', 3), ('e', 3), ('f', 3), ('f#', 3), ('g', 3), ('g#', 3), ('a', 3), ('a#', 3), ('b', 3),
    ('c', 4), ('c#', 4), ('d', 4), ('d#', 4), ('e', 4), ('f', 4), ('f#', 4), ('g', 4), ('g#', 4), ('a', 4), ('a#', 4), ('b', 4),
    ('c', 5), ('c#', 5), ('d', 5), ('d#', 5), ('e', 5), ('f', 5), ('f#', 5), ('g', 5), ('g#', 5), ('a', 5), ('a#', 5), ('b', 5),
    ('c', 6), ('c#', 6), ('d', 6), ('d#', 6), ('e', 6), ('f', 6), ('f#', 6), ('g', 6), ('g#', 6), ('a', 6), ('a#', 6), ('b', 6),
    ('c', 7), ('c#', 7), ('d', 7), ('d#', 7), ('e', 7), ('f', 7), ('f#', 7), ('g', 7), ('g#', 7), ('a', 7), ('a#', 7), ('b', 7),
    ('c',8)
    ]

flatOrder=[
    ('a',0),('bb',0),('b',0),
    ('c', 1), ('db', 1), ('d', 1), ('eb', 1), ('e', 1), ('f', 1), ('gb', 1), ('g', 1), ('ab', 1), ('a', 1), ('bb', 1), ('b', 1),
    ('c', 2), ('db', 2), ('d', 2), ('eb', 2), ('e', 2), ('f', 2), ('gb', 2), ('g', 2), ('ab', 2), ('a', 2), ('bb', 2), ('b', 2),
    ('c', 3), ('db', 3), ('d', 3), ('eb', 3), ('e', 3), ('f', 3), ('gb', 3), ('g', 3), ('ab', 3), ('a', 3), ('bb', 3), ('b', 3),
    ('c', 4), ('db', 4), ('d', 4), ('eb', 4), ('e', 4), ('f', 4), ('gb', 4), ('g', 4), ('ab', 4), ('a', 4), ('bb', 4), ('b', 4),
    ('c', 5), ('db', 5), ('d', 5), ('eb', 5), ('e', 5), ('f', 5), ('gb', 5), ('g', 5), ('ab', 5), ('a', 5), ('bb', 5), ('b', 5),
    ('c', 6), ('db', 6), ('d', 6), ('eb', 6), ('e', 6), ('f', 6), ('gb', 6), ('g', 6), ('ab', 6), ('a', 6), ('bb', 6), ('b', 6),
    ('c', 7), ('db', 7), ('d', 7), ('eb', 7), ('e', 7), ('f', 7), ('gb', 7), ('g', 7), ('ab', 7), ('a', 7), ('bb', 7), ('b', 7),
    ('c',8)
    ]

#######
# XML PARSE FUNCTION WRITTEN BY DAVID YANG
#
#######
def Parse(path,inTempo=None,tiesOn=True,skipPercussion=False):
    xmldoc = minidom.parse(path)
    try:
        tempo=int(xmldoc.getElementsByTagName('sound')[0].getAttribute('tempo'))
    except:
        print('no tempo found')
        tempo=inTempo if inTempo!=None else 120#int(input('What is the tempo of the piece?'))
    completeSong={}
    for part in xmldoc.getElementsByTagName('part'):
        if skipPercussion and part.getElementsByTagName('unpitched')!=[]:continue
        instrument=part.getAttribute('id')
        completeSong[instrument]=parseInstrument(part,tiesOn)
    result=[]
    for part in completeSong:
        for voice in completeSong[part]:
            result.append(voice)
    #print(result)
    return (result,tempo)

def parseInstrument(part,tiesOn):
    partID=part.getAttribute('id')
    print(partID)
    try:
        transpose=int(part.getElementsByTagName('chromatic')[0].childNodes[0].nodeValue)
        #print(transpose)
    except:
        transpose=0
    measures=part.getElementsByTagName('measure')
    key0=part.getElementsByTagName('fifths')[0].childNodes[0].nodeValue
    key=key0
    divisions=int(part.getElementsByTagName('divisions')[0].childNodes[0].nodeValue)
    try:noOfBeats=int(part.getElementsByTagName('beats')[0].childNodes[0].nodeValue)
    except:noOfBeats=4
    try:beatType=beatTypes[part.getElementsByTagName('beat-type')[0].childNodes[0].nodeValue]
    except:beatType=4
    try:beatUnit=beatUnits[part.getElementsByTagName('beat-unit')[0].childNodes[0].nodeValue]
    except:beatUnit=1
    aV=part.getElementsByTagName('voice')
    allVoices=set([aV[i].childNodes[0].nodeValue
         for i in range(len(aV))])
    ties=dict()
    song={}
    repeatStart=(0,False) # measure no and whether repeated once or not
    i=0
    while i <len(measures):

        measure=measures[i]

        if measure.getElementsByTagName('beats')!=[]:
            noOfBeats=int(measure.getElementsByTagName('beats')[0].childNodes[0].nodeValue)
        if measure.getElementsByTagName('beat-type')!=[]:
            beatType=beatTypes[measure.getElementsByTagName('beat-type')[0].childNodes[0].nodeValue]
        if measure.getElementsByTagName('beat-unit')!=[]:
            beatUnit=beatUnits[measure.getElementsByTagName('beat-unit')[0].childNodes[0].nodeValue]
        if (measure.getElementsByTagName('sound')!=[] and
                (measure.getElementsByTagName('words')==[])):
            sound=measure.getElementsByTagName('sound')
            for k in range(len(sound)):
                if sound[k].hasAttribute("tempo"):
                    newTempo=sound[k].getAttribute('tempo')
                    for voice in song:
                        song[voice].append(int(float(newTempo)))
                    break
        if measure.getElementsByTagName('fifths')!=[]:
            key=measure.getElementsByTagName('fifths')[0].childNodes[0].nodeValue

        notes=measure.getElementsByTagName('note')
        sharps=[]
        flats=[]
        naturals=[]
        for note in notes:
            flag=False
            # ignore grace notes
            if (note.getElementsByTagName('grace')!=[]):
                continue

            # for rests
            if note.getElementsByTagName('rest')!=[]:
                pitch='r'
                octave='4'

            # for notes
            elif note.getElementsByTagName('step')!=[]:
                pitch= note.getElementsByTagName('step')[0].childNodes[0].nodeValue.lower()
                octave = note.getElementsByTagName('octave')[0].childNodes[0].nodeValue

            try:
                duration=note.getElementsByTagName('duration')[0].childNodes[0].nodeValue
                temp=(int(duration)/divisions)*beatUnit
            except:
                types = note.getElementsByTagName('type')
                temp = types[0].childNodes[0].nodeValue
                if(temp == "whole"):temp = 'w'
                elif(temp == "half"):temp = 'h'
                elif(temp == "quarter"):temp = 'q'
                elif(temp == "eighth"):temp = 'e'
                elif(temp == "16th"):temp = 's'
                elif(temp == "32nd"):temp='th'
                else:print(temp)
                if temp in noteTypes:
                    temp=noteTypes[temp]
                temp*=beatUnit

            # Accidentals
            try:
                alter=note.getElementsByTagName('alter')[0].childNodes[0].nodeValue
                if alter=='1':
                    pitch+='#'
                elif alter=='-1':
                    pitch+='b'
                elif alter=='-2':
                    pitch=flatOrder[flatOrder.index((pitch,4))-2][0]
                elif alter=='2':
                    pitch=sharpOrder[sharpOrder.index((pitch,4))+2][0]
            except: pass

            if pitch=='b#':
                pitch='c'
                octave=str(int(octave)+1)
            elif pitch=='cb':
                pitch='b'
                octave=str(int(octave)-1)
            elif pitch=='e#':
                pitch='f'
            elif pitch=='fb':
                pitch='e'
            # Transposing
            if pitch!='p' and pitch!='r':
                if pitch[-1]=='#':
                    index=sharpOrder[sharpOrder.index((pitch,int(octave)))+transpose]
                    pitch=index[0]
                    octave=str(index[1])
                else:
                    index=flatOrder[flatOrder.index((pitch,int(octave)))+transpose]
                    pitch=index[0]
                    octave=str(index[1])

            # for percussion
            if (note.getElementsByTagName('unpitched')!=[] or
                note.getElementsByTagName('notehead')!=[]):
                pitch='p'
                octave='1'

            voice=note.getElementsByTagName('voice')[0].childNodes[0].nodeValue
            # final formatting
            string = "%s %s %s" % (pitch,octave,temp)

            # skip tie starts
            if tiesOn and note.getElementsByTagName('tie')!=[]:
                tieList=note.getElementsByTagName('tie')
                for n in range(len(tieList)):
                    tie=tieList[n].getAttribute('type')
                    #print(i)
                    if tie=='start':
                        s=string.split()
                        tPitch=s[0]
                        tOctave=s[1]
                        tTemp=float(s[-1])
                        ties[(tPitch,tOctave)]=tTemp
                        #print('start',voice,string)
                        flag=True
                    elif tie=='stop':
                        #print(ties)
                        # concatenate tied notes on stop
                        string=connectTied(ties,(pitch,octave),temp,voice)
                        #print('stop',voice,string)
            if flag: #skips start of ties
                continue

            voiceList=song.get(voice,[])
            # put chords in tuples
            if note.getElementsByTagName('chord')==[]:
                song[voice]=voiceList+[string]
            else:
                if isinstance(voiceList[-1],tuple):
                    voiceList[-1]=voiceList[-1]+tuple([string])
                else:
                    voiceList[-1]=(voiceList[-1],string)
                    song[voice]=voiceList
            #print(i,voice,string)
        i+=1
        if measure.getElementsByTagName('repeat')!=[]:
            direction=measure.getElementsByTagName('repeat')[0].getAttribute('direction')
            if direction=='forward' and repeatStart[1]==False:
                repeatStart=(i-1,False)
            elif direction=='backward' and repeatStart[1]==False:
                i=repeatStart[0]
                repeatStart=(i,True)
            elif direction=='backward' and repeatStart[1]==True:
                repeatStart=(0,False)

        # adds rests to fill in for unmarked voices in the measure
        for voice in allVoices:
            voices=measure.getElementsByTagName('voice')
            if voice not in [voices[i].childNodes[0].nodeValue for i in range(len(voices))]:
                a=song.get(voice,[])
                b=noOfBeats*beatType
                a.append('r 4 %d' % b)
                song[voice]=a
    final=[]
    for voice in song:
        final.append(song[voice])

    return final


# concatenates noteType of two tied notes
def connectTied(ties,note,time,voice):
    #print(voice,note,time)
    (pitch,octave)=note
    try:
        if (pitch+'b',octave) in ties:
            note=(pitch+'b',octave)
        elif (pitch+'#',octave) in ties:
            note=(pitch+'#',octave)
        elif (pitch[0],octave) in ties:
            note=(pitch[0],octave)
    except:
        for tie in ties:
            if (pitch+'b',octave)==tie:
                note=(pitch+'b',octave)
            elif (pitch+'#',octave)==tie:
                note=(pitch+'#',octave)
            elif (pitch[0],octave)==tie:
                note=(pitch[0],octave)
    try:
        time0=ties[note]
        del ties[note]
        newTime=time0+time
    except:
        print('failed to find tie start')
        newTime=time
    return note[0]+' '+note[1]+' '+str(newTime)

def testLengths(filename,inTempo=None,tiesOn=True):
    file,tempo=Parse(filename,inTempo=inTempo,tiesOn=tiesOn)
    lengths=[]
    for voice in file:
        voiceLength=0
        for chord in voice:
            if isinstance(chord,str):
                voiceLength+=float(chord.split()[2])
            elif isinstance(chord,tuple):
                voiceLength+=float(chord[0].split()[2])
        lengths.append(voiceLength*44100*60/tempo)
    print(lengths)
    mx=max(lengths)
    mn=min(lengths)
    diff=str((mx-mn)/mx*100)+'% difference'
    print(diff)
