

import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from QuTouTiao.items import QutoutiaoItem
import json
import time

class QuSpider(scrapy.Spider):
    name = 'QuTouTiao'
    allowed_domains = ['qutoutiao.net', 'qktoutiao.com']

    bash_url = 'http://api.1sapp.com/content/outList?cid='
    mid_url = '&tn=1&page='
    end_url = '&limit=100&user=temporary1534345404402&show_time=&min_time=&content_type=1&dtu=200'

    '''&limit=10&user=temporary1534345404402&show_time=1534608545989&min_time=1534608120000&content_type=1&dtu=200'''

    pageNames = {
        # '6': '娱乐',
        # '255': '推荐',
        # '1': '热点',
        # '42': '健康',
        # '5': '养生',
        # '4': '励志',
        # '7': '科技',
        # '8': '生活',
        '10': '财经'
        # '9': '汽车',
        # '18': '星座',
        # '12': '美食',
        # '14': '时尚',
        # '16': '旅行',
        # '17': '育儿',
        # '13': '体育',
        # '15': '军事',
        # '23': '历史',
        # '30': '收藏',
        # '19': '游戏',
        # '28': '国际',
        # '40': '新时代',
        # '50': '房产',
        # '51': '家居',
    }

    """
    in qutoutiap api : page is of no use!!!!! 
    # the most important fields : 
       (1) limit: max can set to 100, at here i set it to 100 to decrease uncertain
       (2) min_time param *********** 
          case limit set to 100: 
          ------------------
           when min_time in api is 1560908221000 (2019-6-19 09:37:01)
           response in first time:
               min_time: 1560906659000 (2019-6-19 09:10:59)   --- 
               max_time: 1560908216000 (2019-6-19 09:36:56)
           response in second time : 
                min_time:  1560904891000:(2019-6-19 08:41:31) 
                max_time:  1560906360000: (2019-6-19 09:06:00) 
          --------------------
          when min_time in api is 1560906659000 (2019-6-19 09:10:59)
          response in first time:
               min_time: 1560905203000 (2019-6-19 8:46:43)
               max_time: 1560906644000 (2019-6-19 9:10:44)
          response in second time:
               min_time: 1560903527000 (2019-6-19 8:18:47)
               max_time: 1560905185000 (2019-6-19 8:46:25)

          ---------------------

        从上面可以看出: 在每次结果反馈中， 返回的每条结果的 publish_info的时间值是位于response中 min_time与max_time之间的
        而且只有奇数次访问，才能得到时间段合理的数据。 
        故，请求次序如下: 
        I. request: https:///xxx?limit=100&min_time=1560908221000&xxxx 
        II. GET min_time field from response, At here is 1560906659000
        III. request: https:///xxx?limit=100&min_time=1560906659000&xxxx   
        IV. GET min_time field from response, At here is 1560905203000
        V. request: 

        总结： 看来是通过min_time来进行数据的滚动的！！而且仅限于第一次请求！！！！！
        每次解析出来min_time 然后进行遍历即可

      


    """


    def start_requests(self):
        for num, value in self.pageNames.items():
            for i in range(5):  # only scrapy the first 5 pages of each category(cid)
                url = self.bash_url + str(num) + self.mid_url + str(i+1) + self.end_url
                print('start crawl news list ' + url)
                yield Request(url, callback=self.parse, meta={'type': value})


    def parse(self, response):
        json_res = json.loads(response.body.decode('utf-8'))
        news_list = json_res['data']['data']
        for news in news_list:
            news_url = news['detail_url'] # detail url contains main part of content using json format 
            news_stat_info = {
                'read_cnt': news.get('read_count', 0),
                'share_cnt': news.get('share_count', 0),
                'comment_cnt': news.get('comment_count', 0),
                'people_comment_cnt': news.get('people_comment_count', 0),
                'member_id': news.get('member_id', 'UNK'),
                'follow_num': news.get('follow_num', 0),
                'follow_num_show': news.get('follow_num_show', 0),
                'publish_time': news.get('publish_time', -1)
            }
        
            print('start crawl news content ' + news_url)
            yield Request(news_url, callback=self.get_news_brief, meta={'stat_info': news_stat_info})


    def get_news_brief(self, response):
        news_brief_json = json.loads(response.body.decode('utf-8'))
        # news_id = news_brief_json['id']
        item = QutoutiaoItem()
        news_stat_info = response.meta['stat_info']
        print(response.meta)
        print(type(response.meta))
        item = {
            "news_id": news_brief_json.get('id',''),
            "title": news_brief_json.get('title', ''),
            "source": news_brief_json.get('source', ''),
            "url": news_brief_json.get('url', ''),
            "create_time": news_brief_json.get('createTime', ''),
            "publish_info": news_brief_json.get('publish_info', ''),
            "detail": news_brief_json.get('detail', ''),
            "keywords": news_brief_json.get('keywords', ''),
            "description": news_brief_json.get('description', ''),
            "source_site": news_brief_json.get('sourceSite', '') ,
            "is_origin": news_brief_json.get('isOrigin', -1) ,
            "need_statement": news_brief_json.get('needStatement', ''),
            "source_name": news_brief_json.get('sourceName', '') ,
            "authorid": news_brief_json.get('authorid', ''), 
            "share_cnt": news_stat_info.get('share_cnt', -1),
            "people_comment_cnt": news_stat_info.get("people_comment_cnt", -1),
            "follow_num_show": news_stat_info.get("follow_num_show", -1),
            "read_cnt": news_stat_info.get("read_cnt", -1), 
            "comment_cnt": news_stat_info.get("comment_cnt", -1),
            "member_id": news_stat_info.get("member_id", -1), 
            "follow_num": news_stat_info.get("follow_num", -1),
            "publish_time": news_stat_info.get("publish_time", ''),
            "is_clean": 0,
            "ctime":  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "mtime":  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }
        yield item 