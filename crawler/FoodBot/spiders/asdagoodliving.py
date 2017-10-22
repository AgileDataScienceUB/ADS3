# -*- coding: utf-8 -*-
import scrapy


class AsdagoodlivingSpider(scrapy.Spider):
    name = 'asdagoodliving'
    allowed_domains = ['asdagoodliving.co.uk']
    start_urls = ['http://asdagoodliving.co.uk/']

    def parse(self, response):
        pass
