#coding=utf-8

import os
import traceback
import tornado.ioloop
import tornado.web
from config import kUploadSavePath, kFaceDBPath, kLogFile
from errorNum import *
from PLogger import Logger
from FaceRecgModel import FaceRecgModel
from ImgTool import img2Base64, getImgTypeByFileName
from UuidTool import genUuidByFileName, genUuidRandom
from jsonTool import generateJsonRetStr


class RecgInMemForHtmlHandler(tornado.web.RequestHandler):
    def initialize(self, database):
        if not os.path.exists(kUploadSavePath):
            os.makedirs(kUploadSavePath)

        self.__logger =  Logger()
        self.__faceRecgModel = database


    def get(self):
        self.write('you should have post request')

    def post(self):
        self.__logger.info('receive a request from client')
        try:
            upFileBin = self.__getUploadFile()
            if upFileBin == None:
                return
            # self.__logger.info('file uploaded, save name is ' + upFile)
            # id, thumb, similarity, name, title, intro
            id, thumb, similarity, name, title, intro = self.__faceRecgModel.findIidentityByImageBin(upFileBin)
            # id, thumb, similarity = '1',  '1010100103_thumb.jpg', 0.6
            self.__logger.info(' id is ' + id + ' similarity is ' + str(similarity))

            # img to base64 and trans to client.
            imgFullPath = os.path.join(kFaceDBPath, thumb)
            imgBase64 = img2Base64(imgFullPath)
            ext = getImgTypeByFileName(thumb)[1:]
            jsonStr = '{"errCode":"0","id":"' + id + '","thumb":"' + imgBase64 + '","ext":"' + ext + '","name":"' + name + '","title":"' + title + '","intro":"' + intro + '"}'
            # self.__logger.info('ret str is ' + jsonStr)
            self.write(jsonStr)

            items = [ext, imgBase64,]
            self.render('../html/recgResult.html', items=items)
        except:
            f=open(kLogFile + '.error','a')
            traceback.print_exc(file=f)
            f.flush()
            f.close()
            unknownError =  generateJsonRetStr(UNKONON_ERROR)
            self.write(unknownError)

    '''
    文件上传，返回文件保存信息
    '''
    def __getUploadFile(self):
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

        randomStr = genUuidRandom()
        uploadedFileName = genUuidByFileName(randomStr)
        uploadedFileSavePathWithName = os.path.join(kUploadSavePath, uploadedFileName + '.jpg')
        with open(uploadedFileSavePathWithName, 'wb') as up:
            up.write(fileMeta['body'])
        self.__logger.info("file saved name is " + uploadedFileSavePathWithName)

        return fileMeta['body']