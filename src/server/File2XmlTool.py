#coding=utf-8
import os
import shutil
import time
from UuidTool import *
from PLogger import Logger
from xmlTool import saveXml2File
import re
import sys


reload(sys)
sys.setdefaultencoding('utf-8')

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from xml.dom import minidom

__author__ = 'Administrator'
import sys
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')

class Bath2Xml():
    def __init__(self, picPath, dstPath, xmlFile):
        if not os.path.exists(picPath):
            print(picPath + ' do not exists')
            exit(1)

        self.__picPath = picPath
        self.__dstPath = dstPath
        self.__xmlFile = xmlFile
        self.__xmlRoot = ET.Element('users')
        self.__logger =  Logger()

    def __checkXml(self):
        # 检查环境
        usersXmlFullPath = os.path.join(dstPath, xmlFile)
        if os.path.exists(usersXmlFullPath):
            print('[WARNING] ' + usersXmlFullPath + ' exists')
            exit(2)

        return True

    def __genUserNode(self, userName, userID, userTitle, userIntro, userThumb, userImg, userFeature, status = 1):
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

        return userNode

    def __saveXml2File(self, xmlStr, saveFile):
        saveXml2File(xmlStr, saveFile)

    def extractNameFromDir(self,dir):
        ret = None

        for tmpFile in os.listdir(dir):
            tmpFile = tmpFile.decode('gbk').encode('utf-8')
            ret = self.extractNameFromFileName(tmpFile)
            if ret != None:
                break

        if ret == None:
            ret = 'empty','empty','empty','empty'
        return ret

    def extractNameFromFileName(self, picPath):
        splits = picPath.split('-')
        if len(splits) != 4:
            return None

        position = splits[0]
        location = splits[1]
        title = splits[2]

        tmpName = splits[3]
        nameSplits = tmpName.split('（')
        if len(nameSplits) != 2:
            return None

        name = nameSplits[0]

        return position, location, title, name

    def converts(self):
        # 先检查一下xml文件是否存在
        if not os.path.exists(dstPath):
            os.makedirs(dstPath)

        self.__checkXml()

        fileNum = 0
        for list in os.listdir(picDir):
            list = list.decode('gbk').encode('utf-8')
            nxtDir = os.path.join(picDir, list)
            if not os.path.isdir(nxtDir):
                print '[WARNING] ' + nxtDir + ' is not dir'
                continue

            position, location, title, name = self.extractNameFromDir(nxtDir)

            for files in os.listdir(nxtDir):
                files = files.decode('gbk').encode('utf-8')
                fileNum += 1
                if fileNum % 100 == 0:
                    print 'Processing ' + str(fileNum) + ' files'

                ## 根据文件后缀判断输入格式
                baseName, extStr = os.path.splitext(files)
                if extStr.lower() != '.jpg':
                    self.__logger.error("图片格式非法:" + files + ' id is ' + list)
                    print ("图片格式非法:" + files + ' id is ' + list)
                    continue
                files = files.decode('utf-8').encode('gbk')
                picFullPath = os.path.join(nxtDir, files)
                fileTmpNewNameFullPath = os.path.join(dstPath, files)
                if os.path.exists(fileTmpNewNameFullPath):
                    print '[WARNNING] ' + fileTmpNewNameFullPath + ' exists'
                    #os.remove(picFullPath)
                    exit(1)

                # 拷贝文件，并用uuid重命名，原始的名称不一定适合 比如 中文等等，易出现乱码
                shutil.copy2(picFullPath, dstPath)
                fileMainPath, ext = os.path.splitext(fileTmpNewNameFullPath)
                uuid = genUuidByFileName()
                uuidWithExt = uuid + ext
                finalName = os.path.join(dstPath, uuidWithExt)
                os.rename(fileTmpNewNameFullPath, finalName)
                featureBin = genUuidByFileName() + '.bin'

                #position, location, title, name = self.extractNameFromDir(nxtDir)
                userName = name
                userID = list
                userTitle = title
                userIntro = position
                userThumb = uuidWithExt
                userImg = uuidWithExt
                userFeature = featureBin
                status = 1

                userNode = self.__genUserNode(userName, userID, userTitle, userIntro, userThumb, userImg, userFeature)
                self.__xmlRoot.append(userNode)
        #         self.__saveXml2File(ET.tostring(self.__xmlRoot), os.path.join(dstPath, xmlFile))
        # print(self.__xmlRoot)
        # print (ET.tostring(self.__xmlRoot))
        self.__saveXml2File(ET.tostring(self.__xmlRoot), os.path.join(dstPath, xmlFile))

        print('xml file processed ok')
        print('xml file saved at ' + os.path.join(dstPath, xmlFile))

    def collectHavePhoto(self, fileName):
        tree = ET.parse(fileName)
        i = 0
        root = tree.getroot()
        file_no_photo = open('d:/nophoto.csv', 'w')
        file_have_photo = open('d:/havephoto.csv', 'w')

        # file_object.write(all_the_text)
        # file_object.close( )
        dictNoResult = {}
        dicHaveResult = {}
        for child in root:
            i = i + 1
            # child.set('name', '用户' + str(i))
            status = child.find('status')
            idStr = child.get('id')
            statusStr = status.text

            ## 统计没有照片的
            if statusStr == '0':
                if idStr in  dictNoResult.keys():
                    num = dictNoResult.get(idStr)
                    num = num + 1
                    dictNoResult[idStr] = num
                else:
                    dictNoResult[idStr] = 1

            ## 统计有照片的数目
            if statusStr == '1':
                if idStr in  dicHaveResult.keys():
                    num = dicHaveResult.get(idStr)
                    num = num + 1
                    dicHaveResult[idStr] = num
                else:
                    dicHaveResult[idStr] = 1
        # str = ''
        for key in dictNoResult.keys():
            lastStr = key + ',' + str(dictNoResult[key]) + '\n'
            file_no_photo.write(lastStr)

        for key in dicHaveResult.keys():
            lastStr = key + ',' + str(dicHaveResult[key]) + '\n'
            file_have_photo.write(lastStr)

    def collectNoPhoto(self, fileName):
        tree = ET.parse(fileName)
        i = 0
        root = tree.getroot()
        file_object = open('d:/thefile.csv', 'w')
        # file_object.write(all_the_text)
        # file_object.close( )
        dictResult = {}
        for child in root:
            i = i + 1
            # child.set('name', '用户' + str(i))
            status = child.find('status')
            idStr = child.get('id')
            statusStr = status.text
            if statusStr == '0':
                if idStr in  dictResult.keys():
                    num = dictResult.get(idStr)
                    num = num + 1
                    dictResult[idStr] = num
                else:
                    dictResult[idStr] = 1
        # str = ''
        for key in dictResult.keys():
            lastStr = key + ',' + str(dictResult[key]) + '\n'
            file_object.write(lastStr)


        def batchModifyXML(self, fileName):
            tree = ET.parse(fileName)
        i = 0
        root = tree.getroot()
        for child in root:
            i = i + 1
            child.set('name', '用户' + str(i))
            userName = child.find('displayName')
            userName.text = '用户' + str(i)

            title = child.find('title')
            title.text = '职位' + str(i)

            intro = child.find('intro')
            intro.text = '介绍' + str(i)
        self.__saveXml2File(ET.tostring(root), fileName)


if __name__ == '__main__':
    print('begin to process files from dir')
    picDir = 'D:/work/summitMetting0408/summit-2016-04-08-pruned-2'
    # picDir = 'D:/work/summitMetting0408/summit-2016-04-08'
    dstPath = 'D:/work/summitMetting0408/facedbAfterDel'
    xmlFile = 'users.xml'

    bath2Xml = Bath2Xml(picDir, dstPath, xmlFile)
    bath2Xml.converts()

    # checkXmlFile = 'D:/work/summitMetting0408/xml/users.xml'
    # bath2Xml.collectHavePhoto(checkXmlFile)

    # while True:
    #     time.sleep(1000)
    # picPath = '营销-北京-个人客户总监三级-李东（证件照）.JPG'
    # ret = bath2Xml.extractNameFromFileName(picPath)
    # print ret
    # bath2Xml.converts()
    # testFile = 'D:/work/svn/nlp/zhangjl/imageIdentify/pacs/facedb/users.xml'
    # bath2Xml = Bath2Xml(picDir, dstPath, xmlFile)
    # bath2Xml.collectNoPhoto(testFile)


