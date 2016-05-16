#coding = utf-8
import os
from UuidTool import *
import cv2

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

__author__ = 'Administrator'
from multiprocessing import Process
import json
import requests

def __getChildTextByTag(element, tag):
    ret = None
    for ssonOfRoot in element.iter(tag):
        ret = ssonOfRoot.text
    return ret


def worker(num):
    xmlFile = 'D:/work/summitMetting0408/facedbAfterDel/users.xml'
    print 'parsing user xml file ' + xmlFile
    usersTree = ET.ElementTree(file = xmlFile)
    usersRoot = usersTree.getroot()

    xmlBasePath = 'D:/work/summitMetting0408/facedbAfterDel'
    lineNum = 0
    for sonOfRoot in usersRoot:
        if lineNum % 100 == 0:
            print 'processing ' + str(lineNum)
        lineNum = lineNum + 1

        id = sonOfRoot.attrib['id']
        img = __getChildTextByTag(sonOfRoot, 'img')
        status = __getChildTextByTag(sonOfRoot, 'status')
        if(status == '0'):
            continue
        imgFullPath = ''
        if img.lower().endswith('.jpg') or img.lower().endswith('.jpeg') or img.lower().endswith('.jpeg') or img.lower().endswith('.bmp') or img.lower().endswith('.png'):
            imgFullPath = os.path.join(xmlBasePath, img)
            if not os.path.exists(imgFullPath):
                print('img file ' + imgFullPath + ' not exists, ignoring')
                continue
        url = ''
        if num % 2 == 0:
            url = 'http://192.168.100.72:8088/recognition'
        else:
            url = 'http://192.168.100.71:8088/recognition'

        image = cv2.imread(imgFullPath)
        cv2.flip(image, 1, image)
        fileNameWithPath = 'd:/4delete/' + genUuidByFileName() + '.jpg'
        cv2.imwrite(fileNameWithPath, image)

        files = {'file': open(fileNameWithPath, 'rb')}

        r = requests.post(url, files=files)
        jsonObj = json.loads(r.text)
        tid = jsonObj['id']
        if lineNum % 100 == 0:
            print 'req id is ' + id + ' ret id is ' + tid + ' file is ' + imgFullPath + 'revert is ' + fileNameWithPath

        if tid.strip() != id.strip():
            if num % 2 == 0:
                print 'req id is ' + id + ' ret id is ' + tid + ' file is ' + imgFullPath + 'revert is ' + fileNameWithPath +  ' from 72'
            else:
                print 'req id is ' + id + ' ret id is ' + tid + ' file is ' + imgFullPath + 'revert is ' + fileNameWithPath + ' from 71'

if __name__ == '__main__':
    jobs = []
    for i in range(0,2):
        p = Process(target= worker, args=(i,))
        jobs.append(p)
        p.start()