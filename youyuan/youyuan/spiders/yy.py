# -*- coding: utf-8 -*-
import scrapy, re
from scrapy.linkextractors import LinkExtractor
#from scrapy.spiders import CrawlSpider, Rule
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from youyuan.items import YouyuanItem


class YySpider(RedisCrawlSpider):
    name = 'yy'
    #allowed_domains = ['www.hongniang.com']
    redis_key = "yyspider:start_urls"
    #start_urls = ['http://www.hongniang.com/index/search?sort=0&wh=0&sex=2&starage=0&province=%E5%B9%BF%E4%B8%9C&city=%E6%B7%B1%E5%9C%B3&marriage=0&edu=0&income=8&height=0&pro=0&house=0&child=0&xz=0&sx=0&mz=0&hometownprovince=0']

    page_links = LinkExtractor(allow=r'&page=\d+')
    profile_links = LinkExtractor(allow=r'/user/member/id/\d+')

    rules = (
        Rule(page_links),
        Rule(profile_links, callback='parse_item'),
    )

    # def __init__(self, *args, **kwargs):
    #     # Dynamically define the allowed domains list.
    #     domain = kwargs.pop('domain', '')
    #     self.allowed_domains = filter(None, domain.split(','))
    #     super(YySpider, self).__init__(*args, **kwargs)

    def parse_item(self, response):
        item = YouyuanItem()
        item['username'] = self.get_username(response)
        item['age'] = self.get_age(response)
        item['images_url'] = self.get_image_url(response)
        item['content'] = self.get_content(response)
        item['birthplace'] = self.get_birthplace(response)
        item['education'] = self.get_education(response)
        item['income'] = self.get_income(response)
        item['hobby'] = self.get_hobby(response)
        item['source_url'] = response.url
        item['source'] = "zhongguohongniang"
        yield item

    def get_username(self, response):
        username = response.xpath("//div[@class='name nickname']/text()").extract()
        if len(username):
            username = username[0]
        else:
            username = "NULL"
        return username.strip()

    def get_age(self, response):
        username = response.xpath('//div[@class="sub2"]/div[@class="info1"][4]/div[@class="right"][1]/ul[2]/li[1]/text()').extract()
        if len(username):
            username = username[0]
        else:
            username = "NULL"
        return username.strip()

    def get_image_url(self, response):
        username = response.xpath('//ul[@id="tFocus-pic"]//@src').extract()
        if len(username):
            username = ",".join(username)
        else:
            username = "NULL"
        return username.strip()

    def get_content(self, response):
        content = response.xpath('//div[@class="text"]/text()').extract()
        if len(content):
            content = content[0]
        else:
            content = "NULL"
        return content.strip()

    def get_birthplace(self, response):
        birthplace = response.xpath('//div[@class="info1"][1]/div[@class="right"]/ul[2]/li[1]/text()').extract()
        if len(birthplace):
            birthplace = birthplace[0]
        else:
            birthplace = "NULL"
        return birthplace.strip()

    def get_education(self, response):
        education = response.xpath('//div[@class="info2"]//ul[2]/li[2]/text()').extract()
        if len(education):
            education = education[0]
        else:
            education = "NULL"
        return education.strip()

    def get_income(self, response):
        income = response.xpath('//div[@class="info2"]//ul[3]/li[1]/text()').extract()
        if len(income):
            income = income[0]
        else:
            income = "NULL"
        return income.strip()

    def get_hobby(self, response):
        hobby = response.xpath('//div[@class="info1"][3]//ul[1]/li[1]/text()').extract()
        if len(hobby):
            hobby = "".join(hobby)
        else:
            hobby = None
        return hobby.strip()
