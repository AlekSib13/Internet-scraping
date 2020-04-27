# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline
import scrapy

class PhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['pictures']:
            for picture in item['pictures']:
                try:
                    yield scrapy.Request(picture.replace('82','600'))
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['pictures']=[element[1] for element in results if results[0]]
        return item

class LeroymerlenPipeline(object):
    def __init__(self):
        client=MongoClient('localhost',27017)
        self.mongo_base=client.leroymerlin_test2

    # def characteristics_processing (self,item,spider):
    #     li=item['characteristics']
    #     for element in li:
    #


    def process_item(self, item, spider):
        collection=self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

