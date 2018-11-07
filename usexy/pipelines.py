# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request, log
from scrapy.exceptions import DropItem

class UsexyPipeline(object):
    def process_item(self, item, spider):
        return item

class IndexDownloadPipeline(ImagesPipeline):
    # 使用'/'分割链接，使用最后的部分作为文件名
    def file_path(self, request, response=None, info=None):
        url = request.url
        file_name = url.split('/')[-1]
        return file_name

    #通过 get_media_requests 方法为每一个图片链接生成请求
    def get_media_requests(self, item, info):
        for url in item['urls']:
            # print('-- 1.:', url)
            headers = {
                "Referer": 'http://usexy.me'
            }
            yield Request(url, headers = headers)

    # 单个 item 完成下载时的处理方法
    def item_completed(self, results, item, info):
        print('=== results: ', results)
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Image Downloaded Failed')
        return item