

import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from QuTouTiao.items import QutoutiaoItem
import json
from urllib.parse import urlparse, parse_qs
# import QuTouTiao.spiders.ImageUrlTool as ImageUrlTool
import time

class QuSpider(scrapy.Spider):
    name = 'QuTouTiao'
    allowed_domains = ['qutoutiao.net', 'qktoutiao.com']

    bash_url = 'http://api.1sapp.com/content/outList?cid='
    mid_url = '&tn=1&page='
    end_url = '&limit=10&user=temporary1534345404402&show_time=&min_time=&content_type=1&dtu=200'

    '''&limit=10&user=temporary1534345404402&show_time=1534608545989&min_time=1534608120000&content_type=1&dtu=200'''

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

    def start_requests(self):
        for num, value in self.pageNames.items():
            for i in range(5):  # only scrapy the first 5 pages of each category(cid)
                url = self.bash_url + str(num) + self.mid_url + str(i+1) + self.end_url
                print('&&&&&&&&&&爬取列表' + url)
                yield Request(url, callback=self.parse, meta={'type': value})


    def parse(self, response):
        dict = json.loads(response.body)
        infos = dict['data']['data']
        for info in infos:
            info_url = info['url']
            que = urlparse(info_url).query
            params = parse_qs(que)

            print('&&&&&&&&&&开始爬取:' + info_url)
            yield Request(info_url, callback=self.getInfo, meta={'type': response.meta['type'], 'contentId': params['content_id'][0]})

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

            continue # shuai 
            qi_img_url = ImageUrlTool.uploadImage(down_img_url)
            img['src'] = qi_img_url
            if imgs.index(img) == 0:
                item['thumbnailPic'] = qi_img_url
        item['contents'] = contents

        yield item