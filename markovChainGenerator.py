import random
from xmlParser import Parse
def Markov(xmlFile):
    data = Parse(xmlFile)
    start_index = 0

    final = []
     # create a list of all words
    for voice in data[0]:
        markov = {i:[] for i in voice}    # i create a dict with the words as keys and empty lists as values

        pos = 0
        while pos < len(voice) - 1:    # add a word to the word-key's list if it immediately follows that word
            markov[voice[pos]].append(voice[pos+1])
            pos += 1

        new = {k:v for k,v in zip(range(len(markov)), [i for i in markov])}    # create another dict for the seed to match up with
        length_sentence = random.randint(100, 100)    # create a random length for a sentence stopping point

        seed = random.randint(0, len(new) - 1)    # randomly pick a starting point

        sentence_data = [new[start_index]]     # use that word as the first word and starting point
        current_word = new[start_index]

        while len(sentence_data) < length_sentence:
            next_index = random.randint(0, len(markov[current_word]) - 1)    # randomly pick a word from the last words list.
            next_word = markov[current_word][next_index]
            sentence_data.append(next_word)
            current_word = next_word

        final.append([i for i in sentence_data])
    return (final,data[1])

print(Markov('mario medley.xml'))
