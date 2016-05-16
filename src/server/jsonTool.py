#coding=utf-8
__author__ = 'Administrator'

def generateJsonRetStr(errCode, errMsg = '未知错误'):
    strCode = str(errCode)
    ret = '{"errCode":"' + strCode + '","msg":"' + errMsg + '"}'
    return ret