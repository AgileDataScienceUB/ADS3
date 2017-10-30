# -*- coding: utf-8 -*-
import scrapy


class SeriouseatsSpider(scrapy.Spider):
    name = 'seriouseats'
    allowed_domains = ['seriouseats.com']
    start_urls = ['http://seriouseats.com/']

    def parse(self, response):
        pass
