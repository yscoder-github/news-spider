import pymongo 


def get_newest_by_publish_time():
    conn = pymongo.MongoClient(host='localhost', port=27017)
    news_info_cur = conn.qutoutiao_db.news_brief_collect.find().sort('publish_time', pymongo.DESCENDING).limit(1)
    return news_info_cur[0].get('news_id', ''), news_info_cur[0].get('publish_time', '')


import logging

logging.basicConfig(filename="./log/exec.log", filemode="w", format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')
