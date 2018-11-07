# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from usexy.items import UsexyItem

class IndexSpider(Spider):
    name = 'index'
    allowed_domains = ['usexy.me']
    start_urls = ['http://usexy.me/']

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, cookies={'ftusexyme': '1'})

    def parse(self, response):

        # 获取总页码
        pagetext = response.xpath('//div[@id="primary"]//div[@class="total"]/span/text()').extract_first()
        totalpages = int(pagetext.split(',')[0].split('/')[1][:-1])
        # print('-- totalpages: ', totalpages)

        # 生成所有页面的链接请求
        base_url = "http://usexy.me/page/"
        for num in range(1, totalpages + 1):
            url = base_url + str(num)
            yield Request(url, self.parse)

        # 生成单页每一位模特的入口链接请求
        modellinks = response.xpath('//div[contains(@class, "content-no-sidebar")]//article//a[@rel="bookmark"]/@href').extract()
        # print('== modellinks: ', modellinks)
        for link in modellinks:
            yield Request(link, self.parse_single)

    def parse_single(self, response):
        modelimgs = response.xpath('//article[1]/div[@class="entry-content"]//p/img/@src').extract()
        title = response.xpath('//article[1]/div[@class="entry-content"]//p/img/@alt').extract_first()
        # print('-=-=- modelimgs: %s; title: %s ' % (modelimgs, title))
        item = UsexyItem()
        item['urls'] = modelimgs
        item['title'] = title
        yield item
