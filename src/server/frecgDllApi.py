#coding=utf-8
import ctypes
from ctypes import *
import numpy as np
import os

from config import kDllPath, kModelPath
from errorNum import DIR_NOT_EXISTS, REG_MODEL_INITIAL_ERROR
from PLogger import Logger

__logger = Logger()
if os.path.exists(kDllPath) == False:
    __logger.error("dll path is not exists " + kDllPath)
    exit(DIR_NOT_EXISTS)

# TODO should modify to logger
# print("system path is " + os.getenv("Path"))
systemPath = os.getenv("Path")

# modify path
tmpSystemPath = systemPath + ';' + kDllPath

#modify system path temporarily
os.environ["Path"] = tmpSystemPath

# TODO should modify to logger
__logger.info( 'system path is ' + os.getenv("Path"))
os.chdir(kDllPath)

#is_use_gpu = '1'  #const
fre = ctypes.windll.LoadLibrary('FR_SDK_E_API.dll')
#在python中使用别人的函数库，以下是原型声明

fre.D_multi_init.argtypes = [ctypes.c_char_p, ctypes.c_bool, ctypes.c_char_p]
fre.D_multi_init.restypes = ctypes.c_int

fre.D_detect.argtypes = [ctypes.c_char_p,ctypes.c_void_p]
fre.D_detect.restypes = ctypes.c_int

fre.D_get_feature_by_three_points.argtypes = [ctypes.c_char_p,ctypes.c_void_p,ctypes.c_void_p]
fre.D_get_feature_by_three_points.restypes = ctypes.c_int

## new added
fre.D_get_feature_by_three_points_and_image_data.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_bool]
fre.D_get_feature_by_three_points_and_image_data.restypes = ctypes.c_int
fre.D_detect_by_image_data.argtypes = [ctypes.c_void_p,ctypes.c_void_p]
fre.D_detect_by_image_data.restypes = ctypes.c_int


def FRE_Initialize(model_path, param = None):
    __logger.info( 'initialing model path ' + model_path)
    is_use_gpu = 1
    gpu_id = '0'
    ret = fre.D_multi_init(model_path.encode(), is_use_gpu, gpu_id.encode())
    if ret == 0:
        __logger.info('face recg model initial ok ' + model_path)
    else:
        __logger.info( 'initialed model path ' + model_path + ' ret is ' + str(ret))
        exit(REG_MODEL_INITIAL_ERROR)

    return ret

def FRE_GetFeature(image_path, feature):
    three_point = np.zeros([1, 6], np.int32)
    ret = fre.D_detect(image_path, ctypes.c_void_p(three_point.ctypes.data))
    __logger.info( 'after detect_by_image_data ' + str(ret))
    if ret != 0:
        __logger.error(image_path + ' feature extract error')
        print 'feature extract error from file' + image_path
        return None
    else:
        #__logger.info(image_path + ' feature extract ok ')
        return fre.D_get_feature_by_three_points(image_path, ctypes.c_void_p(three_point.ctypes.data), ctypes.c_void_p(feature.ctypes.data),)

def FRE_GetFeatureInMemory(img, feature):
    three_point = np.zeros([1, 6], np.int32)
    
    ret = fre.D_detect_by_image_data(img, ctypes.c_void_p(three_point.ctypes.data))
    __logger.info( 'after detect_by_image_data ' + str(ret))
    to_norm_feature_flag = 1

    if ret != 0:
        __logger.error('img bin feature extract error')
        print 'feature extract error from bin file'
        return None
    else:
        return fre.D_get_feature_by_three_points_and_image_data(img, ctypes.c_void_p(three_point.ctypes.data), ctypes.c_void_p(feature.ctypes.data),to_norm_feature_flag)

def FRE_GetSimilarity(feature1, feature2, score):
    ret = np.dot(feature1.reshape(-1), feature2.reshape(-1))
    score[0] = ret
    return ret

if __name__ == '__main__':
    FRE_Initialize(os.path.join(kModelPath, 'E_model_main_one.txt'))