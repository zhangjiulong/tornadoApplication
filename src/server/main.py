#coding=utf-8
import sys

import tornado.ioloop
import tornado.httpserver
import tornado.web

from config import kPort
from PLogger import Logger
from UserXmlModel import UserXmlModel
from FaceRecgModel import FaceRecgModel

from handlers import FaceRecgHandler, FaceRecgInMemHandler, RecgForHtmlHandler, RecgInMemForHtmlHandler, IndexHandler, RegisterHandler, RegisterMainHandler

reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')

__author__ = 'Administrator'

if __name__ == '__main__':
    logger = Logger()
    userModel = UserXmlModel()
    faceRecgModel = FaceRecgModel(userModel)
    app=tornado.web.Application(
        handlers=[
        (r'/recognition4File',FaceRecgHandler,dict(database=faceRecgModel)),
        (r'/recognition',FaceRecgInMemHandler,dict(database=faceRecgModel)),
        (r'/recognitionInMem',FaceRecgInMemHandler,dict(database=faceRecgModel)),
        (r'/recognition4html',RecgForHtmlHandler,dict(database=faceRecgModel)),
        (r'/recgInMemForHtml',RecgInMemForHtmlHandler,dict(database=faceRecgModel)),
        (r'/register',RegisterHandler, dict(database=faceRecgModel)),
        (r'/registerMain',RegisterMainHandler),
        (r'/',IndexHandler, dict(database=userModel)),
        ]
    )
    logger.info("pacs system started...")
    print 'pacs system started...'
    app.listen(kPort)
    tornado.ioloop.IOLoop.instance().start()
