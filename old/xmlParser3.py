# fix ties across bars
# recognize time signature changes
# multi instrument


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

beatTypes={
    '4':1,
    '8':1,
    '2':2,
}

noteTypes={'q':1,'dq':1.5,'h':2,'dh':3,'w':4,'e':.5,'de':.75,'tr':1/3,'t':1/3,
    's':.25,'ds':.375,'th':.125,'2t':2/3,
    'q,t':4/3,'h,t':7/3,'dh,t':10/3,'h,2t':8/3,'e,t':.5+1/3,'e,2t':.5+2/3,
    'tw':1/6,'sx':1/6,'q,2t':1+2/3,'s,s':.5,'e,e':1,'q,e':1.5,'e,s':.625,'w,h':6,
    'e,th':.5+1/8,'q,th':1+1/8,'h,e':2.5,'h,s':2.25,'q,s':1.25,'dq,q':2.5,
    'dq,e':2,'dh,e':3.5,'dh,dq':4.5,'dq,s':1.75,'dh,q':4,'dq,dq':3,'dq,de':1.5+.75
    }


def Parse(path):
    xmldoc = minidom.parse(path)

    measures=xmldoc.getElementsByTagName('measure')
    key0=xmldoc.getElementsByTagName('fifths')[0].childNodes[0].nodeValue
    key=key0
    divisions=int(xmldoc.getElementsByTagName('divisions')[0].childNodes[0].nodeValue)
    noOfBeats=int(xmldoc.getElementsByTagName('beats')[0].childNodes[0].nodeValue)
    beatType=beatTypes[xmldoc.getElementsByTagName('beat-type')[0].childNodes[0].nodeValue]
    awhetsgafgn=xmldoc.getElementsByTagName('voice')
    allVoices=set([awhetsgafgn[i].childNodes[0].nodeValue
         for i in range(len(awhetsgafgn))])

    song={}
    last=''
    repeatStart=(0,False) # measure no and whether repeated once or not
    i=0
    while i <len(measures):
        measure=measures[i]

        if measure.getElementsByTagName('sound')!=[] and measure.getElementsByTagName('sound')[0].hasAttribute('tempo'):
            newTempo=measure.getElementsByTagName('sound')[0].getAttribute('tempo')
            for voice in song:
                song[voice].append(int(newTempo))

        notes=measure.getElementsByTagName('note')
        sharps=[]
        flats=[]
        naturals=[]
        for note in notes:
            # ignore grace notes
            if note.getElementsByTagName('grace')!=[]: continue
            # for notes
            if note.getElementsByTagName('step')!=[]:
                pitch= note.getElementsByTagName('step')[0].childNodes[0].nodeValue.lower()
                octave = note.getElementsByTagName('octave')[0].childNodes[0].nodeValue
   
            else:
            # for rests
                pitch='r'
                octave='4'
            try:
                duration=note.getElementsByTagName('duration')[0].childNodes[0].nodeValue
                temp=(int(duration)/divisions)*beatType
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
                temp*=beatType

            # may not be necessary
            # if note.getElementsByTagName("time-modification")!=[]:
            #     normal=note.getElementsByTagName('normal-notes')[0].childNodes[0].nodeValue
            #     actual=note.getElementsByTagName('actual-notes')[0].childNodes[0].nodeValue
            #     temp*=(int(normal)/int(actual))

            # Accidentals
            try:
                alter=note.getElementsByTagName('alter')[0].childNodes[0].nodeValue
                if alter=='1':
                    pitch+='#'
                elif alter=='-1':
                    pitch+='b'

            except:
                if note.getElementsByTagName('accidental')!=[]:
                    accidental=note.getElementsByTagName('accidental')[0].childNodes[0].nodeValue
                    if accidental=='sharp':
                        pitch+='#'
                        sharps.append(pitch[0]) 
                        flats.remove(pitch[0]) if pitch[0] in flats else None
                        naturals.remove(pitch[0]) if pitch[0] in naturals else None
                    elif accidental=='flat':
                        pitch+='b'
                        flats.append(pitch[0])
                        sharps.remove(pitch[0]) if pitch[0] in sharps else None
                        naturals.remove(pitch[0]) if pitch[0] in naturals else None
                    elif accidental=='natural':
                        pitch=pitch[0]
                        naturals.append(pitch[0])
                        flats.remove(pitch[0]) if pitch[0] in flats else None
                        sharps.remove(pitch[0]) if pitch[0] in sharps else None
                else:
                # adds accidental if one was earlier in the measure
                    if pitch in sharps: pitch+='#'
                    elif pitch in flats: pitch+='b'
                    elif pitch in naturals: pitch=pitch[0]
                    # applies key signature
                    else:
                        if pitch in keys[key]:
                            if int(key)>0:
                                pitch+='#'
                            elif int(key)<0:
                                pitch+='b'

            # final formatting
            string = "%s %s %s" % (pitch,octave,temp)
            # skip tie starts
            if note.getElementsByTagName('tie')!=[]:
                tie=note.getElementsByTagName('tie')[0].getAttribute('type')
                if tie=='start':
                    last=string
                    continue
                elif tie=='stop':
                    # concatenate tied notes on stop
                    string=connectTied(last,string)

            voice=note.getElementsByTagName('voice')[0].childNodes[0].nodeValue
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
                a.append('r 4 %d'%noOfBeats*beatType)
                song[voice]=a
    final=[]
    for voice in song:
        final.append(song[voice])
    tempo=int(xmldoc.getElementsByTagName('per-minute')[0].childNodes[0].nodeValue)
    return (final,tempo)


# concatenates noteType of two tied notes
def connectTied(l,s):
    L=l.split()
    S=s.split()
    value=float(L[-1])+float(S[-1])
    return str(S[0])+' '+str(S[1])+' '+str(value)

def testLengths(filename):
    file,tempo=Parse(filename)
    lengths=[]
    for voice in file:
        voiceLength=0
        for chord in voice:
            if isinstance(chord,str):
                voiceLength+=float(chord.split()[-1])
            elif isinstance(chord,tuple):
                voiceLength+=float(chord[0].split()[-1])
        lengths.append(voiceLength*44100*60/tempo)
    print(lengths)
    mx=max(lengths)
    mn=min(lengths)
    diff=str((mx-mn)/mx*100)+'% difference'
    print(diff)

#testLengths('smash bros.xml')

print(Parse('pirates.xml'))