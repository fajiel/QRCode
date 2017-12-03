

import redis
import requests
import traceback
import json
import time
import logging

logging.basicConfig(filename='/var/log/check_domain.log', level=logging.INFO)

API = 'http://vip.weixin139.com/weixin/2053259644.php?domain='

if __name__ == '__main__':
    redis_cli = redis.Redis()
    namelist = redis_cli.smembers('namelist')
    logging.info(namelist)
    for domain in namelist:
        try:
            resp = requests.get(API+domain,timeout=10)
        except:
            logging.error(traceback.format_exec())
            redis_cli.sadd('ban_namelist',domain)
        data = json.loads(resp.text)
        logging.info(data)
        if data['status'] == '2':
            redis_cli.srem('namelist',domain)
            logging.info('remove domain {}'.format(domain) )
            time.sleep(10)

