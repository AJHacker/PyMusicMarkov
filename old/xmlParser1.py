def Parse(path):
    from xml.dom import minidom
    import string

    xmldoc = minidom.parse(path)

    notes=xmldoc.getElementsByTagName('note')

    song={}

    last=''

    for note in notes:
        if note.getElementsByTagName('step')!=[]:
            pitch= note.getElementsByTagName('step')[0].childNodes[0].nodeValue.lower()
            octave = note.getElementsByTagName('octave')[0].childNodes[0].nodeValue    
        else:
            pitch='r'
            octave='4'
        
        types = note.getElementsByTagName('type')
        temp = types[0].childNodes[0].nodeValue
        if(temp == "whole"):temp = 'w'
        elif(temp == "half"):temp = 'h'
        elif(temp == "quarter"):temp = 'q'
        elif(temp == "eighth"):temp = 'e'
        elif(temp == "16th"):temp = 's'
        else:print(temp)

        # accidentals and dots
        if note.getElementsByTagName('dot')!=[]:
            temp='d'+temp
        if note.getElementsByTagName('accidental')!=[]:
            accidental=note.getElementsByTagName('accidental')[0].childNodes[0].nodeValue
            if accidental=='sharp':
                pitch+'#'
            else:
                pitch+'b'

        # final formatting
        string = "%s %s %s" % (pitch,octave,temp)

        voice=note.getElementsByTagName('voice')[0].childNodes[0].nodeValue
        voiceList=song.get(voice,[])
        if note.getElementsByTagName('chord')==[]:
            song[voice]=voiceList+[string]
        else:
            if isinstance(voiceList[-1],tuple):
                voiceList[-1]=voiceList[-1]+tuple([string])
            else:
                voiceList[-1]=(voiceList[-1],string)
                song[voice]=voiceList

    final=[]
    for voice in song:
        final.append(song[voice])
    return final


print(Parse('uptown funk.xml'))