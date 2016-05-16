#coding=utf-8

__author__ = 'Administrator'
import os
import traceback
import tornado.ioloop
import tornado.web
from config import kUploadSavePath, kFaceDBPath, kLogFile
from PLogger import Logger
from UuidTool import genUuidByFileName, genUuidRandom
from jsonTool import *
from errorNum import *


class AppBaseHandler(tornado.web.RequestHandler):
    def initialize(self, database):
        if not os.path.exists(kUploadSavePath):
            os.makedirs(kUploadSavePath)

        self.__logger =  Logger()
        self.__expRecgModel = database

    def get(self):
        self.write('you should have post request')

    def post(self):
        self.__logger.info('receive a request from client')
        try:
            upFile = self.__getUploadFileOnlySave2Disk()
            if upFile == None:
                return

            self.__logger.info('file uploaded, save name is ' + upFile)
            # id, thumb, similarity, name, title, intro

            smile = self.__expRecgModel.getExpFromImg(upFile)
            description = 'normal'
            faceNo = 1
            if smile>0:
                description = 'smile'
                faceNo = 2

            # jsonStr = '{"errCode":"0","faceNo":' + str(faceNo) + ',"decription":"' + description + '"}'
            jsonStr = '{"errCode":"0","score":' + str(smile) + ',"faceNo":' + str(faceNo) + ',"decription":"' + description + '"}'
            # jsonStr = '{"errCode":"0","id":"' + id + '","thumb":"' + imgBase64 + '","ext":"' + ext + '","}'

            # self.__logger.info('ret str is ' + jsonStr)
            self.write(jsonStr)
        except:
            f=open(kLogFile + '.error','a')
            traceback.print_exc(file=f)
            f.flush()
            f.close()
            unknownError =  generateJsonRetStr(UNKONON_ERROR)
            self.write(unknownError)

    '''
    文件上传，返回文件内存中的二进制部分
    '''
    def getUploadFileOnlyInMem(self):
        self.__logger.info("receiving a file from client")
        #check if upload file more than 1 then return error
        fileMetas = []
        try:
            #do some thing you need
            fileMetas = self.request.files['file']
        except Exception as e:
            retErrStr = generateJsonRetStr(SHOULD_UPLOAD_ONE_JPG_FILE, '请上传一张图片以供识别')
            self.write(retErrStr)
            return None
            #error: has not attribute
        fileMetas = self.request.files['file']
        if 1 != len(fileMetas):
            self.__logger.error("upload file num is not 1")
            retErrStr = generateJsonRetStr(PIC_NUM_SHOUD_ONE, 'upload file num is not 1')
            self.write(retErrStr)
            return None

        #check if upload file type is not jpg then return error
        fileMeta = fileMetas[0]
        oriFileName = fileMeta['filename']
        baseName, extStr = os.path.splitext(oriFileName)
        if extStr.lower() != '.jpg':
            self.__logger.error("upload file type is not jpg")
            retErrStr = generateJsonRetStr(PIC_TYPE_SHOUD_JPG, 'upload file type is not jpg')
            self.write(retErrStr)
            return None
        self.__logger.info('file saved in memory')

        return fileMeta['body']


    '''
    文件上传，保存文件到磁盘，并返回文件名
    '''
    def getUploadFileOnlySave2Disk(self):
        self.__logger.info("receiving a file from client")
        #check if upload file more than 1 then return error
        fileMetas = []
        try:
            #do some thing you need
            fileMetas = self.request.files['file']
        except Exception as e:
            retErrStr = generateJsonRetStr(SHOULD_UPLOAD_ONE_JPG_FILE, '请上传一张图片以供识别')
            self.write(retErrStr)
            return None
            #error: has not attribute
        fileMetas = self.request.files['file']
        if 1 != len(fileMetas):
            self.__logger.error("upload file num is not 1")
            retErrStr = generateJsonRetStr(PIC_NUM_SHOUD_ONE, 'upload file num is not 1')
            self.write(retErrStr)
            return None

        #check if upload file type is not jpg then return error
        fileMeta = fileMetas[0]
        oriFileName = fileMeta['filename']
        baseName, extStr = os.path.splitext(oriFileName)
        if extStr.lower() != '.jpg':
            self.__logger.error("upload file type is not jpg")
            retErrStr = generateJsonRetStr(PIC_TYPE_SHOUD_JPG, 'upload file type is not jpg')
            self.write(retErrStr)
            return None

        # begin uploaded file
        randomStr = genUuidRandom()
        uploadedFileName = genUuidByFileName(randomStr)
        uploadedFileSavePathWithName = os.path.join(kUploadSavePath, uploadedFileName + '.jpg')
        with open(uploadedFileSavePathWithName, 'wb') as up:
            up.write(fileMeta['body'])
        self.__logger.info("file saved name is " + uploadedFileSavePathWithName)

        return uploadedFileSavePathWithName

    '''
    文件上传，返回内存部分，并在本地保存一份，返回文件名
    '''
    def getUploadFileSave2DiskAnd2Mem(self):
        self.__logger.info("receiving a file from client")
        #check if upload file more than 1 then return error
        fileMetas = []
        try:
            #do some thing you need
            fileMetas = self.request.files['file']
        except Exception as e:
            retErrStr = generateJsonRetStr(SHOULD_UPLOAD_ONE_JPG_FILE, '请上传一张图片以供识别')
            self.write(retErrStr)
            return None,None
            #error: has not attribute
        fileMetas = self.request.files['file']
        if 1 != len(fileMetas):
            self.__logger.error("upload file num is not 1")
            retErrStr = generateJsonRetStr(PIC_NUM_SHOUD_ONE, 'upload file num is not 1')
            self.write(retErrStr)
            return None,None

        #check if upload file type is not jpg then return error
        fileMeta = fileMetas[0]
        oriFileName = fileMeta['filename']
        baseName, extStr = os.path.splitext(oriFileName)
        if extStr.lower() != '.jpg':
            self.__logger.error("upload file type is not jpg")
            retErrStr = generateJsonRetStr(PIC_TYPE_SHOUD_JPG, 'upload file type is not jpg')
            self.write(retErrStr)
            return None, None

        # begin uploaded file
        randomStr = genUuidRandom()
        uploadedFileName = genUuidByFileName(randomStr)
        uploadedFileSavePathWithName = os.path.join(kUploadSavePath, uploadedFileName + '.jpg')
        with open(uploadedFileSavePathWithName, 'wb') as up:
            up.write(fileMeta['body'])
        self.__logger.info("file saved name is " + uploadedFileSavePathWithName)

        return uploadedFileSavePathWithName, fileMeta['body']