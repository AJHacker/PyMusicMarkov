#WEB SCRAPES TO GET MXL FILES BASED ON SEARCH TERM

from bs4 import BeautifulSoup
import requests
import urllib.parse
import zipfile
import urllib.request
import shutil
import os
from xml.dom import minidom



def search(query='Enter'):
    secret = 'G6fASjFi6LLNjZ2rgmkmV9VH6SHqde82'
    authkey = 'porcYv8AEiPuBHMNGQJaRoPKo2SgnJpf'
    searchQuery = query

    urlEncode = {'text':searchQuery , 'sort':"view_count"}
    URL = "http://musescore.com/sheetmusic?"+urllib.parse.urlencode(urlEncode)

    r = requests.get(URL)

    soup = BeautifulSoup(r.text,'html.parser')

    wrappers = soup.find_all('div',{ "class" : "wrapper" })

    compositions = []
    increment = 0
    for div in wrappers: #iterate over loop [above sections]
        name = div.find('a').text.encode('ascii', 'ignore').decode()
        views = div.find('span',{ "class" : "views-field-png" }).text.lstrip().rstrip()
        link = 'http://musescore.com'+div.find('a')['href']
        split = link.split('/')
        score = split[-1]
        link='http://api.musescore.com/services/rest/score/'+score+'.xml?oauth_consumer_key='+authkey
        compositions.append((increment,name,views,link, score))
        increment+=1

    return compositions

def download(url,fileName, score):
    file_name='TEMP/temp.xml'
    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    xmldoc = minidom.parse(file_name)
    secret = xmldoc.getElementsByTagName('secret')[0].childNodes[0].nodeValue

    downloadurl = 'http://static.musescore.com/'+score+'/'+secret+'/score.mxl'
    file_name='TEMP/temp.mxl'
    with urllib.request.urlopen(downloadurl) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

    with zipfile.ZipFile("TEMP/temp.mxl","r") as zip_ref:
        zip_ref.extractall("TEMP")
        shutil.rmtree('TEMP/META-INF')
    for filename in os.listdir('TEMP'):
        if filename.endswith(".xml") and filename.startswith('lg'):
            shutil.move('TEMP/'+filename, 'XMLs/'+fileName+'.xml')
