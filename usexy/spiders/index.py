# -*- coding: utf-8 -*-
import scrapy


class IndexSpider(scrapy.Spider):
    name = 'index'
    allowed_domains = ['usexy.me']
    start_urls = ['http://usexy.me/']

    def parse(self, response):
        pass
