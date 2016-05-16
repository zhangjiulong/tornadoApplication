#coding=utf-8
import os
from PLogger import Logger
from UserXmlModel import UserXmlModel

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from config import kModelPath, kFeatureDims, kFaceDBPath, kFacedbXMLName, kFaceFeatureReadFromFile, kFaceFeaturePath, \
    kFaceRecgThreshold, kStopOnIntialFeatureError
from errorNum import *
import numpy as np
from frecgDllApi import FRE_GetFeature, FRE_GetFeatureInMemory, FRE_GetSimilarity, FRE_Initialize


class FaceRecgModel():
    def __init__(self, userXmlModel):
        # pass
        self.__logger = Logger()
        self.__userXmlModel = userXmlModel
        self.__logger.info('initialing FaceRecg Model')
        self.__userXmlModelList = userXmlModel.getUsersList()
        modelPath = os.path.join(kModelPath, 'E_model_main_one.txt')
        # templateModelPath = modelPath + '.template'
        if not os.path.exists(modelPath):
            self.__logger.error("model file do not exists " + kModelPath)
            exit(MODEL_PATH_EMPTY)

        self.__xmlFile = os.path.join(kFaceDBPath, kFacedbXMLName)
        #self.__createModelConfigFromTemplate(modelPath)
        self.__featureDb = []

        ret = FRE_Initialize(modelPath, 1)
        
        self.__logger.info('feature intial ret is ' + str(ret))
        if ret != 0 :
            print 'model intial error exiting'
            exit(MODEL_INITIAL_ERROR)
        self.__logger.info('face recg model initial ok')
        self.__logger.info('initialing feature db')
        print('initialing feature db')
        self.__initFeatureDb()
        self.__logger.info('features initialed ok')
        print('features initialed ok')

    # calculate feature of a img.
    def __fastGetFaceFeature(self, imgPath, binPath):
        feature = np.zeros([1, kFeatureDims], np.float32)
        if kFaceFeatureReadFromFile and os.path.isfile(binPath):
            feature = np.fromfile(binPath, np.float32)
            #self.__logger.info( 'Read feature from file ' + binPath)
            return feature

        tmpFeature = self.__getFeature(imgPath)
        if np.linalg.norm(tmpFeature) > 0.00001:
            tmpFeature.tofile(binPath)
            feature = tmpFeature
        return feature

    def fastGetFaceFeature(self, imgPath, binPath):
        return self.__fastGetFaceFeature(imgPath, binPath)

    def __initFeatureDb(self):
        # print len(self.__userXmlModelList)
        for idx, [id, thumb, featureFile, img, name, displayName, title, intro, ] in enumerate(self.__userXmlModelList):
            if name == '':
                self.__logger.error('id is' + id + ' name do not exits in xml file ' + imgFullPath)
                print 'id is' + id + ' name do not exits in xml file ' + imgFullPath + '\n'
                print 'System existing..........'
                exit(XML_FILE_FILD_LOST_ERROR)

            thumbFullPath = os.path.join(kFaceDBPath, thumb)
            if not os.path.exists(thumbFullPath):
                self.__logger.error('thum file ' + thumb + ' not exists, ignoring')
                print 'file ' + thumb + 'do not exists but saved in xml file '+ kFacedbXMLName + '\n'
                print 'System existing..........'
                exit(FILE_NOT_EXISTS)

            imgFullPath = os.path.join(kFaceDBPath, img)
            binFullPath = os.path.join(kFaceFeaturePath, featureFile)
            if not os.path.exists(imgFullPath):
                self.__logger.error('img file ' + imgFullPath + ' not exists, ignoring')
                print 'file ' + img + 'do not exists but saved in xml file '+ kFacedbXMLName + '\n'
                print 'System existing..........'
                exit(FILE_NOT_EXISTS)

            feature = self.__fastGetFaceFeature(imgFullPath, binFullPath)

            # 无特征时不放入内存，直接掠过
            if np.linalg.norm(feature) <= 0.00001:
                self.__logger.info('processing xml feature exacted error')
                if kStopOnIntialFeatureError:
                    print('processing xml feature exacted')
                    print 'img is ' + imgFullPath + ' extract feature error exiting.'
                    exit(FEATURE_EXTRACT_ERROR)
                #另外设置 xml相应的status为0
                xPathStr = './/user[@id="' + id + '"]'
                #featureFile = feature
                self.__userXmlModel.setStatus0ByXpath(xPathStr, featureFile)
            self.__featureDb.append([id, thumb, feature, img, name, displayName, title, intro, ])
        self.__logger.info( 'after initial feature db size is ' + str(len(self.__featureDb)))

    # id, thumb, similarity, name, title, intro
    def findIdentityByFeature(self, feature):
        if feature.max() == feature.min() == 0:
            return  '0', '0', '0', '0','0', '0'
        scores = np.zeros(len(self.__featureDb), np.float32)
        for idx, [id, thumb, featureInDb, img, name, displayName, title, intro] in enumerate(self.__featureDb):
            similarity = self.getSimilarity(feature, featureInDb)
            scores[idx] = similarity
        index = np.argmax(np.array(scores))
        #增加打印前五的日志
        tmpLen = len(scores)
        printLen = 6
        if printLen > tmpLen:
            printLen = tmpLen
        
        temp = np.argpartition(-np.array(scores), printLen - 1)
        result_args = temp[:printLen - 1]
        for tmpIndex in result_args:
            self.__logger.info('[top 5]id is ' + str(self.__featureDb[tmpIndex][0]) + ' simility is ' + str(scores[tmpIndex]))
        
        #print scores[index]
        if scores[index] > kFaceRecgThreshold:
            return self.__featureDb[index][0], self.__featureDb[index][1], str(scores[index]), self.__featureDb[index][4], self.__featureDb[index][6], self.__featureDb[index][7]
        else:
            return '0', '0', '0', '0','0', '0'

    def findIidentityByImage(self, imgPath):
        feature = self.__getFeature(imgPath)
        return self.findIdentityByFeature(feature)

    def findIidentityByImageBin(self, imgBin):
        feature = self.__getFeatureInMemory(imgBin)
        return self.findIdentityByFeature(feature)

    def __getFeature(self, image_path):
        feature = np.zeros([1, kFeatureDims], np.float32)
        image_path = str(image_path)
        FRE_GetFeature(image_path, feature)
        #print feature
        return feature

    def __getFeatureInMemory(self, imgBin):
        feature = np.zeros([1, kFeatureDims], np.float32)

        FRE_GetFeatureInMemory(imgBin, feature)
        self.__logger.info('imgbin feature extracted')
        #print feature
        return feature

    def getSimilarity(self, feature1, feature2):
        compare_score = np.zeros(1, np.float32)
        FRE_GetSimilarity(feature1, feature2, compare_score)
        return compare_score[0]

    def getUserXMLModel(self):
        return self.__userXmlModel

    #新注册人员特征加入特征库
    def addRegister(self, register):
        self.__featureDb.append(register)

if __name__ == '__main__':
    userXmlModel = UserXmlModel()
    faceRecgModel = FaceRecgModel(userXmlModel)


