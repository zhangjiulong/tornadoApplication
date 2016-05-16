#coding = utf-8
import os

__author__ = 'Administrator'
from multiprocessing import Process
import json
import requests

def worker(num):
    while True:
        print 'worker ' + str(num) + ' is requesting'
        filename = 'D:/work/summitMetting0408/summit-2016-04-08/1010211172/1010211172.jpg'
        basename,ext = os.path.splitext(filename)
        assert(ext=='.jpg' or ext=='.JPG')
        url = ''
        tmpNum = num % 3
        if tmpNum == 0:
            url = 'http://192.168.100.71:8088/recognition'
        elif tmpNum == 1:
            url = 'http://192.168.100.72:8088/recognition'
        else:
            url = 'http://192.168.100.32:8088/recognition'

        files = {'file': open(filename, 'rb')}

        r = requests.post(url, files=files)
        jsonObj = json.loads(r.text)
        print 'img str is' + jsonObj['errCode']
        #base642Img(jsonObj['thumb'])
        print r.text
    return

if __name__ == '__main__':
    jobs = []
    for i in range(0,31):
        p = Process(target= worker, args=(i,))
        jobs.append(p)
        p.start()