# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QutoutiaoItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    time = scrapy.Field()
    reference = scrapy.Field()
    content = scrapy.Field()
    contents = scrapy.Field()
    uniqueValue = scrapy.Field()
    topicName = scrapy.Field()
    thumbnailPic = scrapy.Field()