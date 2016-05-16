#coding=utf-8
import json
import requests
import os
import sys
import time
import random
#filename = sys.argv[1]
from config import kFaceDBPath, KTESTFILE
from ImgTool import base642Img
from timeTool import *

while True:
    filename = 'D:/work/svn/nlp/zhangjl/imageIdentify/pacs/facedb/1010100103_img.jpg'
    basename,ext = os.path.splitext(filename)
    assert(ext=='.jpg' or ext=='.JPG')

    url = 'http://192.168.100.132:8088/recognition'
    files = {'file': open(filename, 'rb')}
    startTime = getMicSecTime()
    r = requests.post(url, files=files)
    jsonObj = json.loads(r.text)
    print 'ret is ' + jsonObj['errCode']
    #base642Img(jsonObj['thumb'])
    print r.text
    endTime = getMicSecTime()
    print('time used is ' + str(endTime - startTime))
    time.sleep(1)
