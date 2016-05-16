import time

__author__ = 'Administrator'

def getMicSecTime():
    # ret = datetime.datetime.now()
    ret =  time.time() * 1000.0
    return ret

if __name__ == '__main__':
    print('current time is ' + str(getMicSecTime()))
    curTime = getMicSecTime()
    time.sleep(1)
    print('dif is ' + str(getMicSecTime() - curTime))