

import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from QuTouTiao.items import QutoutiaoItem
# import QuTouTiao.spiders.ImageUrlTool as ImageUrlTool
import json
import time as time_tool


class Babite(scrapy.Spider):
    name = 'Babite'
    allowed_domains = ['8btc.com']
    start_urls = ['http://m.8btc.com/blockchain']
    # bash_url = 'http://m.8btc.com/blockchain/page/'
    bash_url = 'https://app.blockmeta.com/w1/news/list?num=20&page='
    page_base_url = 'https://www.8btc.com/article/'

    headers = {'Cookie':'UM_distinctid=164253c069b3f-02265862c6ddda-47e1137-100200-164253c069eb7;'
                    +'yd_cookie=8ab1eadd-ec8f-4774a72a9d138e474562faf5866cc57a99cb;'
                    +'CNZZDATA5934906=cnzz_eid%3D1004817248-1529628310-null%26ntime%3D1529720185;'
                    +'QINGCLOUDELB=836e074b593c4f44bd48f6f76fb94554c2f4da300bc4aee30249f3e95199a4b3|Wy3Bl|Wy3Ai',
               'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Mobile Safari/537.36'
               }


    def start_requests(self):

        for i in range(3):
            url = self.bash_url + str(i)
            print('&&&&&&&&&&爬取列表' + url)
            yield Request(url, callback=self.parse)

    def parse(self, response):
        print(response.text)
        dict = json.loads(response.body)
        info_list = dict['list']
        for info in info_list:
            content_id = str(info['id'])
            pic_url = info['image']
            page_url = self.page_base_url + content_id
            print('&&&&&&&&&&开始爬取:' + page_url)
            yield Request(page_url, callback=self.parse_page, headers=self.headers, meta={'contentId': '8bit'+content_id, 'thumbnailPic': pic_url})


    def parse_page(self, response):
        item = QutoutiaoItem()
        bsC = BeautifulSoup(response.text, 'lxml')

        sources = bsC.find('div', class_='article-content-title-box')
        '''
        dateStr = sources.find('span', class_='fr').get_text()
        dateObj = datetime.strptime(dateStr, "%Y-%m-%d %H:%M")
        dateStr = datetime.strftime(dateObj, "%Y-%m-%d %H:%M:%S")
        '''

        release_time = time_tool.strftime('-%m-%d %H:%M:%S', time_tool.localtime(time_tool.time()))
        item['time'] = '2099' + release_time

        item['title'] = sources.div.get_text()
        # item['time'] = dateStr
        item['reference'] = sources.find('a', class_='author-a1').get_text()
        item['uniqueValue'] = response.meta['contentId']
        item['topicName'] = '区块链'
        item['thumbnailPic'] = ImageUrlTool.uploadImage(response.meta['thumbnailPic'])

        contents = bsC.find('div', class_='article-content')
        imgs = contents.find_all('img')

        isDel = False
        for content in contents.find_all('p'):

            if content.get_text() == '引用：':
                isDel = True
            if isDel:
                content.decompose()

        for img in imgs:
            del img['height']
            down_img_url = img['src']
            continue # shuai 
            qi_img_url = ImageUrlTool.uploadImage(down_img_url)
            img['src'] = qi_img_url
        item['contents'] = contents

        return item




'''
        bsC = BeautifulSoup(response.text, 'lxml')
        items = bsC.find('div', id='list_content_all').find_all('div', class_="article-hp-info article-hp-big-info big-info category-coin-info")
        for item in items:
            page_url = item.find('a', class_='article-hp-big-pic')['href']
            print('&&&&&&&&&&开始爬取:' + page_url)
            yield Request(page_url, callback=self.parse_page, headers=self.headers, meta={'contentId': page_url})

        for i in range(4):
            url = self.bash_url + str(i)
            yield Request(url, callback=self.parse)
'''
