#coding=utf-8
import os
import sys
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')
from UuidTool import genUuidByFileName

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
# from lxml import etree as LET
# import lxml.etree.ElementTree as LET
# from lxml import etree as ET
from xml.dom import minidom
from config import kFaceDBPath, kFacedbXMLName, kFaceFeaturePath, kDllPath
try:
    from config import KFacedbXMLBAKPath
except ImportError:
    KFacedbXMLBAKPath = None
from PLogger import Logger
from xmlTool import fixedWritexml, saveXml2File
import time
import shutil



__author__ = 'pattern'

class UserXmlModel():

    def __init__(self, xmlFile = os.path.join(kFaceDBPath, kFacedbXMLName)):
        self.__logger = Logger()
        self.__users = []
        self.__userXmlFile = os.path.join(kFaceDBPath, kFacedbXMLName)
        self.__parseUsersXML(xmlFile)
        # sys.setdefaultencoding('utf-8')

    def __getChildTextByTag(self, element, tag):
        ret = None
        for ssonOfRoot in element.iter(tag):
            ret = ssonOfRoot.text
        return ret

    def __parseUsersXML(self, xmlFile = os.path.join(kFaceDBPath, kFacedbXMLName)):
        self.__logger.info('parsing user xml file ' + xmlFile)
        usersTree = ET.ElementTree(file = xmlFile)
        usersRoot = usersTree.getroot()
        self.__usersTree = usersTree
        self.__usersRoot = usersRoot

        for sonOfRoot in usersRoot:
            id = sonOfRoot.attrib['id']
            name = sonOfRoot.attrib['name']
            displayName = self.__getChildTextByTag(sonOfRoot, 'displayName')
            title = self.__getChildTextByTag(sonOfRoot, 'title')
            intro = self.__getChildTextByTag(sonOfRoot, 'intro')
            thumb = self.__getChildTextByTag(sonOfRoot, 'thumb')
            img = self.__getChildTextByTag(sonOfRoot, 'img')
            feature = self.__getChildTextByTag(sonOfRoot, 'feature')
            status = self.__getChildTextByTag(sonOfRoot, 'status')
            #self.__logger.info( id + ',' +  name + ',' + displayName + ',' + title + ',' + intro + ',' + thumb + ',' + img + ',' + feature + ',' + str(status))
            if(status == '0'):
                continue
            if img.lower().endswith('.jpg') or img.lower().endswith('.jpeg') or img.lower().endswith('.jpeg') or img.lower().endswith('.bmp') or img.lower().endswith('.png'):
                imgFullPath = os.path.join(kFaceDBPath, img)
                binFullPath = os.path.join(kFaceFeaturePath, feature)
                if not os.path.exists(imgFullPath):
                    self.__logger.error('img file ' + imgFullPath + ' not exists, ignoring')
                    continue

                self.__users.append([id, thumb, feature, img, name, displayName, title, intro, ])
        self.__logger.info('user xml file ' + self.__userXmlFile + ' pasrsed ok')
        return sonOfRoot

    def getUsersNum(self):
        return len(self.__users)

    def getUsersList(self):
        return self.__users

    def getUserTree(self):
        return self.__usersTree

    def getUserRoot(self):
        return self.__usersRoot

    def setStatus0ByXpath(self, xPathStr, featureFile, xmlFile = os.path.join(kFaceDBPath, kFacedbXMLName)):
        self.__logger.info('processing xpath ' + str(xPathStr) + ' feature ' + str(featureFile))

        xPathElements = self.getUserRoot().findall(xPathStr)
        for tmpElement in xPathElements:
            tmpFeature = tmpElement.find('feature').text
            if tmpFeature == featureFile:
                statusNode = tmpElement.find('status')
                # tmpElement.set('status', '0')
                # print(statusNode.text)
                statusNode.text = '0'
                # print(statusNode.text)
                saveXml2File(ET.tostring(self.getUserRoot()), xmlFile)

    def bakXml(self, srcFile = os.path.join(kFaceDBPath, kFacedbXMLName), dstFile = (str(time.time()).replace('.','') + genUuidByFileName() + '.xml')):
        if not os.path.exists(KFacedbXMLBAKPath):
            os.makedirs(KFacedbXMLBAKPath)

        dstFileWithPath = os.path.join(KFacedbXMLBAKPath, dstFile)
        shutil.copy2(srcFile, dstFileWithPath)
        self.__logger.info('file ' + srcFile + ' baked to ' + dstFileWithPath)

    def addUser(self, userName, userID, userTitle, userIntro, userThumb, userImg, userFeature, status = 1):
        userNode = ET.Element('user')
        userNode.set('id', userID)
        userNode.set('name', userName)
        displayNode = ET.Element('displayName')
        displayNode.text = userName
        userNode.append(displayNode)
        titleNode = ET.Element('title')
        titleNode.text = userTitle
        userNode.append(titleNode)
        introNode = ET.Element('intro')
        introNode.text = userIntro
        userNode.append(introNode)
        thumbNode = ET.Element('thumb')
        thumbNode.text = userThumb
        userNode.append(thumbNode)
        imgNode = ET.Element('img')
        imgNode.text = userImg
        userNode.append(imgNode)
        featureNode = ET.Element('feature')
        featureNode.text = userFeature
        userNode.append(featureNode)
        statusNode = ET.Element('status')
        statusNode.text = str(status)
        userNode.append(statusNode)
        self.__usersRoot.append(userNode)
        if status == 1:
            self.__users.append([id, userThumb, userFeature, userImg, userName, userName, userTitle, userIntro, ])

        saveXml2File(ET.tostring(self.getUserRoot()), os.path.join(kFaceDBPath, kFacedbXMLName))
        if KFacedbXMLBAKPath:
            self.bakXml()
        pass


if __name__ == '__main__':
     userXmlModel = UserXmlModel('d:/work/svn/nlp/zhangjl/imageIdentify/pacs/facedb/users.xml')
     userXmlModel.addUser('张九龙', '张九龙', '张九龙', '张九龙', 'no', 'img', 'feature', 1)
     # id = '1010106577.jpg'
     # xPathStr = './/user[@id="' + id + '"]'
     # featureFile = '1010106577.jpg.bin'
     # userXmlModel.setStatus0ByXpath(xPathStr, featureFile, 'd:/work/svn/nlp/zhangjl/imageIdentify/pacs/facedb/users.xml')
     # print 'go on'

     # print(str(datetime.now().timetuple()))
     # print(str(time.time()).replace('.',''))
     # userXmlModel.bakXml()