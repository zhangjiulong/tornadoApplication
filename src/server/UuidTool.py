#coding=utf-8
__author__ = 'Administrator'

import uuid

def genUuidRandom():
    id = uuid.uuid4()
    retStr = str(id)
    return retStr
    
def genUuidByFileName(fileName = genUuidRandom()):
    tmpUuid = uuid.uuid4()
    id = uuid.uuid3(tmpUuid, fileName)
    retStr = str(id).encode('utf-8')
    return retStr

if __name__ == '__main__':
    fileName = "ok"
    print(genUuidByFileName())