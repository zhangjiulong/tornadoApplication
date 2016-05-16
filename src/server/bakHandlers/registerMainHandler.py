#coding=utf-8
__author__ = 'pattern'

import tornado.ioloop
import tornado.web

class RegisterMainHandler(tornado.web.RequestHandler):
    def initialize(self):
        pass
        # self.__userXmlModel = database
        # self.__faceRecgModel = database['faceRecgModel']

    def get(self):
        self.render('../html/register.html')
        # self.write("Hello, world " + str(self.__userXmlModel.getUsersNum()))
