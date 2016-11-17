#<attributes>
    #<divisions> this number is the <duration> for a beat
#<time>
    #<beat-type> is the bottom # of the time signature

# todo change <type> to <duration> calculated using above

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
    '8':.5,
    '2':2,
}

def Parse(path):
    from xml.dom import minidom
    import string

    xmldoc = minidom.parse(path)

    measures=xmldoc.getElementsByTagName('measure')
    key0=xmldoc.getElementsByTagName('fifths')[0].childNodes[0].nodeValue
    key=key0
    divisions=xmldoc.getElementsByTagName('divisions')[0].childNodes[0].nodeValue
    beatType=beatTypes[xmldoc.getElementsByTagName('beat-type')[0].childNodes[0].nodeValue]

    song={}
    last=''
    for measure in measures:
        notes=measure.getElementsByTagName('note')
        sharps=[]
        flats=[]
        naturals=[]
        for note in notes:
            # for notes
            if note.getElementsByTagName('step')!=[]:
                pitch= note.getElementsByTagName('step')[0].childNodes[0].nodeValue.lower()
                octave = note.getElementsByTagName('octave')[0].childNodes[0].nodeValue    
            else:
            # for rests
                pitch='r'
                octave='4'
            
            #Old code using type string
            # types = note.getElementsByTagName('type')
            # # try-except to prevent crashing from unknown bug where temp=q
            # # fix later(?)
            # try:
            #     # temp= note type
            #     temp = types[0].childNodes[0].nodeValue
            # except: 
            #     temp='whole'

            # if(temp == "whole"):temp = 'w'
            # elif(temp == "half"):temp = 'h'
            # elif(temp == "quarter"):temp = 'q'
            # elif(temp == "eighth"):temp = 'e'
            # elif(temp == "16th"):temp = 's'
            # elif(temp == '32nd'):temp = 'th'
            # # else for other note types unencountered as of yet
            # else: print(temp)

            # if note.getElementsByTagName('dot')!=[]:
            #     temp='d'+temp

            # Accidentals
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
            if pitch in keys[key]:
                if int(key)>0:
                    pitch+='#'
                elif int(key)<0:
                    pitch+='b'

            # final formatting
            string = "%s %s %s" % (pitch,octave,duration)
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
        # adds rests to fill in for unmarked voices in the measure
        for voice in song:
            voices=measure.getElementsByTagName('voice')
            if voice not in [voices[i].childNodes[0].nodeValue for i in range(len(voices))]:
                song[voice].append('r 4 w')
    final=[]
    for voice in song:
        final.append(song[voice])
    return final


# concatenates noteType of two tied notes
def connectTied(l,s):
    #print(l,s)
    L=l.split()
    S=s.split()
    value=int(L[-1])+int(S[-1])
    return s[:2]+' '+str(value)

#print(Parse('fairy fountain.xml'))