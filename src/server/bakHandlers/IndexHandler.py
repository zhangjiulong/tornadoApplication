#coding=utf-8

__author__ = 'Administrator'

import tornado.ioloop
import tornado.web

class IndexHandler(tornado.web.RequestHandler):
    def initialize(self, database):
        self.__userXmlModel = database
        # self.__faceRecgModel = database['faceRecgModel']

    def get(self):
        self.render('../html/main.html')
        # self.write("Hello, world " + str(self.__userXmlModel.getUsersNum()))
