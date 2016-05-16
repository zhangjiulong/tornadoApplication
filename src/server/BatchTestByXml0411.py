#coding=utf-8
import os
from config import *
import json
import requests

__author__ = 'Administrator'

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

class BatchTestByXml():

    def __getChildTextByTag(self, element, tag):
        ret = None
        for ssonOfRoot in element.iter(tag):
            ret = ssonOfRoot.text
        return ret


    def test(self, xmlFile):
        print 'parsing user xml file ' + xmlFile
        usersTree = ET.ElementTree(file = xmlFile)
        usersRoot = usersTree.getroot()
        self.__usersTree = usersTree
        self.__usersRoot = usersRoot
        myWriter = open('d:/result.csv', 'a')

        xmlBasePath = 'D:/work/summitMetting0408/facedbAfterDel/'
        lineNum = 0
        for sonOfRoot in usersRoot:
            if lineNum % 100 == 0:
                print 'processing ' + str(lineNum)
            lineNum = lineNum + 1

            id = sonOfRoot.attrib['id']
            img = self.__getChildTextByTag(sonOfRoot, 'img')
            status = self.__getChildTextByTag(sonOfRoot, 'status')
            if(status == '0'):
                continue
            imgFullPath = ''
            if img.lower().endswith('.jpg') or img.lower().endswith('.jpeg') or img.lower().endswith('.jpeg') or img.lower().endswith('.bmp') or img.lower().endswith('.png'):
                imgFullPath = os.path.join(xmlBasePath, img)
                if not os.path.exists(imgFullPath):
                    print('img file ' + imgFullPath + ' not exists, ignoring')
                    continue

            url = 'http://192.168.100.30:8088/recognition'
            files = {'file': open(imgFullPath, 'rb')}

            r = requests.post(url, files=files)
            str2write = ''
            try:
                jsonObj = json.loads(r.text)

                tid = jsonObj['id']
                score = jsonObj['score']

                if lineNum % 100 == 0:
                    print 'request id is ' + id + ' ret id is ' + tid
                str2write = 'reqid,' + str(id) + ',retid,' +  str(tid) + ',score,' + str(score) + ',file,' + imgFullPath + '\n'
            except ValueError:
                # print(str2write)
                str2write = 'error,error,error,error \n'
            myWriter.write(str2write)
            myWriter.flush()

if __name__ == '__main__':
    xmlFile = 'D:/work/summitMetting0408/facedbAfterDel/users.xml'
    batchTestByXml = BatchTestByXml()
    batchTestByXml.test(xmlFile)