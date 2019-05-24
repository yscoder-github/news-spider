

import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
# from QuTouTiao.items import QutoutiaoItem
import json
from urllib.parse import urlparse, parse_qs
import time

class QuSpider(scrapy.Spider):
    name = 'Yidian'
    allowed_domains = ['www.yidianzixun.com','toutiao.com']

    bash_url = 'http://api.1sapp.com/content/outList?cid='
    mid_url = '&tn=1&page='
    end_url = '&limit=10&user=temporary1534345404402&show_time=&min_time=&content_type=1&dtu=200'



    # yidian related 

    topic_url = "http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id={}&cstart=0&cend=10&infinite=true&refresh=1&__from__=pc&multi=5&_spt=yz~eaod%3B8%3B%3B%3C%3A28%3D%3F%3E%3A%3B%3A&appid=web_yidian&_=1558657931825"
    url = "http://www.yidianzixun.com/"
    # url = "https://www.toutiao.com/api/pc/feed/?category=news_tech&utm_source=toutiao&widen=1&max_behot_time=1558654072&max_behot_time_tmp=1558654072&tadrequire=true&as=A1154C5E876419F&cp=5CE77481196F5E1&_signature=771aQwAAs2T74YiK0.nRD--9Wl"
    # url = "https://www.toutiao.com/"
    # '''&limit=10&user=temporary1534345404402&show_time=1534608545989&min_time=1534608120000&content_type=1&dtu=200'''
    # url = "https://www.toutiao.com/"
    # yidian 
    cate_names = {
        "12116082754": "娱乐"

    }
    pageNames = {
        '6': '娱乐',
        '255': '推荐',
        '1': '热点',
        '42': '健康',
        '5': '养生',
        '4': '励志',
        '7': '科技',
        '8': '生活',
        '10': '财经',
        '9': '汽车',
        '18': '星座',
        '12': '美食',
        '14': '时尚',
        '16': '旅行',
        '17': '育儿',
        '13': '体育',
        '15': '军事',
        '23': '历史',
        '30': '收藏',
        '19': '游戏',
        '28': '国际',
        '40': '新时代',
        '50': '房产',
        '51': '家居',
    }


    start_urls = (
       url,
    )

    # def start_requests(self):


    #     for num, value in self.cate_names.items():
    #         url = self.url.format(num)
    #         print('&&&&&&&&&&爬取列表' + url)
    #         yield Request(url, callback=self.parse, meta={'type': num}) # meta to follow status for me 

    def parse(self, response):
        print(response)
        yield Request(self.topic_url,
                          callback=self.parse_request) 
    
    def parse_request(self, response):
        print(response)

  
    

    def getInfo(self, response):
        item = QutoutiaoItem()
        bsC = BeautifulSoup(response.text, 'lxml').find('div', class_='article')
        rt = bsC.find('div', class_='info').string
        rtAry = rt.split(' ')

        item['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        item['title'] = bsC.h1.get_text()
        # item['time'] = rtAry[0] + ' ' + rtAry[1]
        item['reference'] = rtAry[2]
        item['uniqueValue'] = response.meta['contentId']
        item['topicName'] = response.meta['type']
        item['thumbnailPic'] = ''

        contents = bsC.find('div', class_='content')
        imgs = contents.find_all('img')

        for img in imgs:
            down_img_url = img['src'] if 'src' in img.attrs.keys() else img['data-src']
        item['contents'] = contents

        yield item