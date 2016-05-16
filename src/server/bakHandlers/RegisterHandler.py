#coding=utf-8
from errorNum import REG_USER_PIC_NUM_SHOULD_TWO, PIC_TYPE_SHOUD_JPG, REG_USER_NAME_IS_EMPTY, REG_PIC_NOT_OK, \
    REG_USER_PIC_SHOULD_HAVE_DISPLAY_PHOTO, REG_USER_PIC_EROR, REG_USER_ID_IS_EMPTY
from errorNum import *
import os
from UuidTool import genUuidRandom, genUuidByFileName
from config import kFaceDBPath, kUploadSavePath, kFaceFeaturePath
from jsonTool import generateJsonRetStr
import numpy as np

__author__ = 'pattern'

import tornado.ioloop
import tornado.web
from PLogger import Logger

class RegisterHandler(tornado.web.RequestHandler):

    def initialize(self, database):
        self.__faceRecgModel = database
        self.__userXmlModel = self.__faceRecgModel.getUserXMLModel()
        self.__logger = Logger()

    def __collectUserInfo(self):
        self.__logger.info("user registering")
        ret = []
        # 获取展示照片
        displayPhoto = self.__uploadJpgFileByFields('displayPhoto')
        if displayPhoto == None:
            return ret

        ret.append(displayPhoto)

        # 获取识别照片（用于提取特征）
        recgPhoto = self.__uploadJpgFileByFields('recgPhoto')
        if recgPhoto == None:
            return ret

        ret.append(recgPhoto)
        self.__logger.info('register pic uploaded ok')
        return ret

    '''
    返回的文件名带有后缀
    '''
    def __uploadJpgFileByFields(self, field):
        self.__logger.info('uploading ' + field + ' pic')
        displayMetas = []
        try:
            #do some thing you need
            displayMetas = self.request.files[field]
        except Exception as e:
            #retErrStr = generateJsonRetStr(REG_USER_PIC_EROR, '注册上传图片错误')
            #self.write(retErrStr)
            return None
        #displayMetas = self.request.files[field]
        if 1 != len(displayMetas):
            self.__logger.error('upload file should have ' + field + ' fields')
            retErrStr = generateJsonRetStr(REG_USER_PIC_EROR, 'upload should have display photo')
            self.write(retErrStr)
            # self.write('{"errCode":"' + str(REG_USER_PIC_NUM_SHOULD_TWO) + '"}')
            return None

        f = displayMetas[0]
        rawName = f['filename']
        rawBaseName, rawExtStr = os.path.splitext(rawName)
        if rawExtStr.lower() != '.jpg':
            self.__logger.error("upload file type is not jpg")
            retErrStr = generateJsonRetStr(PIC_TYPE_SHOUD_JPG, 'upload file type is not jpg')
            self.write(retErrStr)
            # self.write('{"errCode":"' + str(PIC_TYPE_SHOUD_JPG) + '"}')
            return None

        uploadedFileName = genUuidByFileName()
        uploadedFileSavePathWithName = os.path.join(kFaceDBPath, uploadedFileName + '.jpg')
        with open(uploadedFileSavePathWithName, 'wb+') as up:
            up.write(f['body'])
        # up.seek(0)
        return uploadedFileName + '.jpg'
        # ret.append(uploadedFileName + '.jpg')

    def get(self):
        self.write('you should have post request')

    def post(self):
        self.__logger.info('receiving register from client')

        # read parameters from client.
        userName = self.get_argument('userName', 'Empty')
        if userName == '':
            retErrMsg = generateJsonRetStr(REG_USER_NAME_IS_EMPTY, 'user name is empty')
            self.write(retErrMsg)
            # self.write('register error, user name is empty')
            return
        userID = self.get_argument('userID', 'Empty')
        if len(userID) == 0:
            retErrMsg = generateJsonRetStr(REG_USER_ID_IS_EMPTY, 'user ID is empty')
            self.write(retErrMsg)
            # self.write('register error, user name is empty')
            return
            
        userTitle = self.get_argument('userTitle', 'Empty')
        userIntro = self.get_argument('userIntro', 'Empty')
        pics = self.__collectUserInfo()
        if len(pics) != 2:
            retErrMsg = generateJsonRetStr(REG_USER_PIC_NUM_SHOULD_TWO, 'upload file num is not 2')
            self.write(retErrMsg)
            return

        # generate feature
        uuidStr = genUuidByFileName()
        featureFile = uuidStr + '.bin'
        imgPath = os.path.join(kFaceDBPath, pics[1])
        binPath = os.path.join(kFaceFeaturePath, featureFile)
        newFeature = self.__faceRecgModel.fastGetFaceFeature(imgPath, binPath)
        if np.linalg.norm(newFeature) <= 0:
            errStr = generateJsonRetStr(REG_PIC_NOT_OK, '请尝试上传另一张头像照片')
            self.write(errStr)
            return

        # added to user model
        # TODO NEW REGISTER STATUS IS 1
        self.__userXmlModel.addUser(userName, userID, userTitle, userIntro, pics[0], pics[1], featureFile, 1)
        # self.__featureDb.append([id, thumb, feature, img, name, displayName, title, intro, ])
        register = [userID, pics[0], newFeature, pics[1], userName, userName, userTitle, userIntro, ]
        self.__faceRecgModel.addRegister(register)
        self.__logger.info('[NEWREGISTERMSGCELL] [userName]' + userName + ' [userID]' + userID + ' [userTitle]' + userTitle + ' [userIntro]' + userIntro + '[userThumb]' + pics[0] + ' [userImg]' + pics[1] + ' [userFeatureFile]' + featureFile + ' [status]' + '1')
        
        registerOKStr = generateJsonRetStr(0, '注册成功')
        self.write(registerOKStr)
        #self.render('../html/main.html')