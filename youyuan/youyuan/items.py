# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YouyuanItem(scrapy.Item):
    # define the fields for your item here like:
    username = scrapy.Field()
    age = scrapy.Field()
    images_url = scrapy.Field()
    content = scrapy.Field()
    birthplace = scrapy.Field()
    education = scrapy.Field()
    income = scrapy.Field()
    hobby = scrapy.Field()
    source_url = scrapy.Field()
    source = scrapy.Field()
