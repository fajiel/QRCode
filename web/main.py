import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), u".."))

import time
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import logging
from web.utils.util import get_config
CON_DICT = get_config()

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='logs/server_{}.log'.format(time.strftime("%Y_%m_%d", time.localtime())),
                    filemode='w')

# logging.debug('This is debug message')
# logging.info('This is info message')
# logging.warning('This is warning message')

from tornado.options import define, options
define("port",
       default=CON_DICT.get('WEBSERVER',{}).get("port", 8008),
       help="run on the given port",
       type=int,
       )

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        args = self.request.uri.split("?", 1)[-1] if "?" in self.request.uri else ""
        targetUrl = 'http://{}/{}?{}'.format(
            CON_DICT.get('DOMAIN', ""),
            CON_DICT.get('FIELD', ""),
            args
        )

        self.redirect(targetUrl)

class ArgsHandler(tornado.web.RequestHandler):
    def get(self):
        channelId = self.get_argument('c', '')

        androidUrl = 'http://{}/{}'.format(
            CON_DICT.get('DOMAIN', ""),
            CON_DICT.get('FIELD', ""),
        )
        iosUrl = CON_DICT.get('ITUNESURL', "")
        self.render('default.html', androidUrl=androidUrl, iosUrl=iosUrl)

def check_QR():
    print("----checking----",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    pass

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/', IndexHandler),
                  (r'/weixin.sogou.com*', ArgsHandler),
                  ],
        template_path=os.path.join(os.path.dirname(__file__), "templates")
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.PeriodicCallback(check_QR, 1 * 5 * 60 * 1000).start()
    tornado.ioloop.IOLoop.instance().start()
    logging.info('Start web server.')