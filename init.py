import os
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

def init():
    if not (os.path.isdir("WAV")):
        os.makedirs('WAV')
    if not (os.path.isdir("TEMP")):
        os.makedirs('TEMP')
    if not (os.path.isdir("XMLs")):
        os.makedirs('XMLs')
    if not (os.path.exists('data.txt')):
        file = open("data.txt", "w")
        file.close()
    f = open('data.txt','w')
    for item in listFiles('XMLs'):
        f.write(item[5:-4]+'\n')
