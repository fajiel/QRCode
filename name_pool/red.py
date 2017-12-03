#encoding=utf-8

import uuid,json,logging,random,time

import redis

import tornado.ioloop
import tornado.web
from tornado.httpserver import HTTPServer
from tornado.httpclient import AsyncHTTPClient,HTTPRequest


DEBUG = False
PORT  = 7761


name_list = [
    'canzuo5.com',
    'huibiaow.com',
    'aiyart.com',
    'yseego.com',
    'hnsdsny.com'
]

check_url = 'http://vip.weixin139.com/weixin/2053259644.php?domain='

redis_cli = redis.Redis(host='localhost',port=6379,db=0)

class RedHandler(tornado.web.RequestHandler):
    def get(self):
        path = self.get_argument('p')
        namelist = list(redis_cli.smembers('namelist'))
        domain = random.choice(namelist)
        url = 'https://{0}{1}'.format(domain,path)
        self.redirect(url)


application = tornado.web.Application([
    (r"/red/", RedHandler),
    ],debug=DEBUG)

if __name__ == "__main__":
    redis_cli.sadd('namelist',*name_list)
    if DEBUG:
        application.listen(PORT)
        tornado.ioloop.IOLoop.current().start()
    else:
        httpserver = HTTPServer(application)
        httpserver.bind(PORT,'0.0.0.0')
        httpserver.start(4)
        tornado.ioloop.IOLoop.instance().start()

~
~
~
~
