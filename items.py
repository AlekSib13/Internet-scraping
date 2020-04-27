# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose,TakeFirst

# def adjusted_size(element):
#     if element[:3]=='res':
#         return element.replace('82','600')
#     return element

class LeroymerlenItem(scrapy.Item):
    article_number = scrapy.Field()
    article_description = scrapy.Field()
    price = scrapy.Field()
    pictures=scrapy.Field()
    characteristics_detailed=scrapy.Field()
    _id=scrapy.Field()

    # define the fields for your item here like:
    # article_number = scrapy.Field(output_processor=TakeFirst())
    # article_description = scrapy.Field(output_processor=TakeFirst())
    # price = scrapy.Field(output_processor=TakeFirst())
    # pictures=scrapy.Field(input_processor=MapCompose(adjusted_size))
