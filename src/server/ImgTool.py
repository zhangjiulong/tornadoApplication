#coding=utf-8
import base64
import os

__author__ = 'Administrator'
def img2Base64(fileName):
    if os.path.exists(fileName) == False:
        return ''

    f = open(fileName,'rb') #二进制方式打开图文件
    base64Str = base64.b64encode(f.read()) #读取文件内容，转换为base64编码
    f.close()

    return base64Str

def getImgTypeByFileName(fileName):
    pre, ext = os.path.splitext(fileName)
    return ext

def base642Img(base64Str):
    imgBin = None
    if os.path.exists('d:/result.jpg'):
        os.remove('d:/result.jpg')
        print 'deleted file d;/result.jpg'

    imgBin = base64.b64decode(base64Str)
    with open('d:/result.jpg', 'wb') as f:
        f.write(imgBin)
    f.close()


if __name__ == '__main__':
    fileName = "d://wd//dw//1000.txt"
    print getImgTypeByFileName(fileName)