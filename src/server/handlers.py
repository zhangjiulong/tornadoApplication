#coding=utf-8
import os
import traceback
import tornado.ioloop
import tornado.web
from config import *
from errorNum import *
from PLogger import Logger
from ImgTool import img2Base64, getImgTypeByFileName
from UuidTool import genUuidByFileName, genUuidRandom
from jsonTool import *
from AppBaseHandler import AppBaseHandler
import numpy as np

__author__ = 'Administrator'

class FaceRecgHandler(AppBaseHandler):

    def initialize(self, database):
        if not os.path.exists(kUploadSavePath):
            os.makedirs(kUploadSavePath)

        self.__logger =  Logger()
        self.__faceRecgModel = database
        super(self.__class__, self).initialize(database)

    def get(self):
        self.write('you should have post request')

    def post(self):
        self.__logger.info('receive a request from client')
        try:
            upFile = self.getUploadFileOnlySave2Disk()
            if upFile == None:
                return
            self.__logger.info('file uploaded, save name is ' + upFile)
            # id, thumb, similarity, name, title, intro
            id, thumb, similarity, name, title, intro = self.__faceRecgModel.findIidentityByImage(upFile)
            self.__logger.info(upFile + ' id is ' + id + ' similarity is ' + str(similarity) + 'name is ' + name + ' title is ' + title + ' intro is ' + intro)

            # img to base64 and trans to client.
            imgFullPath = os.path.join(kFaceDBPath, thumb)
            imgBase64 = img2Base64(imgFullPath)
            ext = getImgTypeByFileName(thumb)
            # jsonStr = '{"errCode":"0","id":"' + id + '","thumb":"' + imgBase64 + '","ext":"' + ext + '","}'
            jsonStr = '{"errCode":"0","id":"' + id + '","thumb":"' + imgBase64 + '","ext":"' + ext + '","name":"' + name + '","title":"' + title + '","intro":"' + intro + '"}'
            # self.__logger.info('ret str is ' + jsonStr)
            self.write(jsonStr)
        except:
            f=open(kLogFile + '.error','a')
            traceback.print_exc(file=f)
            f.flush()
            f.close()
            unknownError =  generateJsonRetStr(UNKONON_ERROR)
            self.write(unknownError)

class FaceRecgInMemHandler(AppBaseHandler):

    def initialize(self, database):
        if not os.path.exists(kUploadSavePath):
            os.makedirs(kUploadSavePath)

        self.__logger =  Logger()
        self.__faceRecgModel = database
        super(self.__class__, self).initialize(database)

    def get(self):
        self.write('you should have post request')

    def post(self):
        self.__logger.info('receive a request from client')
        try:
            upFile, upFileBin = self.getUploadFileSave2DiskAnd2Mem()
            if upFileBin == None:
                return

            # id, thumb, similarity, name, title, intro
            id, thumb, similarity, name, title, intro = self.__faceRecgModel.findIidentityByImageBin(upFileBin)
            self.__logger.info(upFile + ' id is ' + id + ' similarity is ' + str(similarity) + 'name is ' + name + ' title is ' + title + ' intro is ' + intro)

            # img to base64 and trans to client.
            imgFullPath = os.path.join(kFaceDBPath, thumb)
            imgBase64 = img2Base64(imgFullPath)
            ext = getImgTypeByFileName(thumb)
            # jsonStr = '{"errCode":"0","id":"' + id + '","thumb":"' + imgBase64 + '","ext":"' + ext + '","}'
            jsonStr = '{"errCode":"0","id":"' + id + '","thumb":"' + imgBase64 + '","ext":"' + ext + '","name":"' + name + '","title":"' + title + '","intro":"' + intro + '"}'
            # self.__logger.info('ret str is ' + jsonStr)
            self.write(jsonStr)
        except:
            f=open(kLogFile + '.error','a')
            traceback.print_exc(file=f)
            f.flush()
            f.close()
            unknownError =  generateJsonRetStr(UNKONON_ERROR)
            self.write(unknownError)

class RecgForHtmlHandler(AppBaseHandler):
    def initialize(self, database):
        if not os.path.exists(kUploadSavePath):
            os.makedirs(kUploadSavePath)

        self.__logger =  Logger()
        self.__faceRecgModel = database
        super(self.__class__, self).initialize(database)


    def get(self):
        self.write('you should have post request')

    def post(self):
        self.__logger.info('receive a request from client')
        try:
            upFile = self.getUploadFileOnlySave2Disk()
            if upFile == None:
                return
            self.__logger.info('file uploaded, save name is ' + upFile)
            # id, thumb, similarity, name, title, intro
            id, thumb, similarity, name, title, intro = self.__faceRecgModel.findIidentityByImage(upFile)
            # id, thumb, similarity = '1',  '1010100103_thumb.jpg', 0.6
            self.__logger.info(upFile + ' id is ' + id + ' similarity is ' + str(similarity))

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

class RecgInMemForHtmlHandler(AppBaseHandler):
    def initialize(self, database):
        if not os.path.exists(kUploadSavePath):
            os.makedirs(kUploadSavePath)

        self.__logger =  Logger()
        self.__faceRecgModel = database
        super(self.__class__, self).initialize(database)


    def get(self):
        self.write('you should have post request')

    def post(self):
        self.__logger.info('receive a request from client')
        try:
            upFileBin = self.getUploadFileOnlyInMem()
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

class IndexHandler(tornado.web.RequestHandler):
    def initialize(self, database):
        self.__userXmlModel = database
        # self.__faceRecgModel = database['faceRecgModel']

    def get(self):
        self.render('../html/main.html')
        # self.write("Hello, world " + str(self.__userXmlModel.getUsersNum()))


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

class RegisterMainHandler(tornado.web.RequestHandler):
    def initialize(self):
        pass
        # self.__userXmlModel = database
        # self.__faceRecgModel = database['faceRecgModel']

    def get(self):
        self.render('../html/register.html')
        # self.write("Hello, world " + str(self.__userXmlModel.getUsersNum()))
