# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from leroymerlen.items import LeroymerlenItem
from scrapy.loader import ItemLoader
import re

class LmSpider(scrapy.Spider):
    name = 'LM'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/search/?q=%D0%BE%D0%B1%D0%BE%D0%B8&family=00b9b5a0-faeb-11e9-810b-878d0b27ea5b&suggest=true']

    def __init__(self,search):
        self.start_urls=[f'https://leroymerlin.ru/search/?q={search}&suggest=true']

    def parse(self, response:HtmlResponse):
        stuff_links = response.xpath("//div[@class='product-name']/a/@href").extract()
        for stuff_link in stuff_links:
            yield response.follow(stuff_link,callback=self.stuff_parse)
        next_page=response.xpath("//div[@class='service-panel clearfix pagination-bottom']//div[@class='next-paginator-button-wrapper']/a/@href").extract_first()
        yield response.follow(next_page,callback=self.parse)


    def stuff_parse(self,response:HtmlResponse):
        article_number=response.xpath("//uc-pdp-card-ga-enriched//span[contains(@slot,'article')]/text()").extract_first()
        article_description=response.xpath("//uc-pdp-card-ga-enriched//h1[contains(@slot,'title')]/text()").extract_first()
        price=response.xpath("//uc-pdp-price-view[1]//span[@slot='price']/text()").extract_first()
        currency=response.xpath("//uc-pdp-price-view[1]//span[@slot='currency']/text()").extract_first()
        unit=response.xpath("//uc-pdp-price-view[1]//span[@slot='unit']/text()").extract_first()
        pictures=response.xpath("//img[@slot='thumbs']/@src").extract()
        characteristics=response.xpath("//dl[@class='def-list']//div[@class='def-list__group']").extract()
        for element in characteristics:
            li=[]
            characteristic1 = response.xpath("//dl[@class='def-list']//div[@class='def-list__group']//dt[@class='def-list__term']/text()").extract()
            characteristic2 = response.xpath("//dl[@class='def-list']//div[@class='def-list__group']//dd[@class='def-list__definition']/text()").extract()
            total=li.append({'-':characteristic1,'--':characteristic2})

        yield LeroymerlenItem(article_number=article_number,
                              article_description=article_description,
                              price=f'{price} {currency}/{unit}',
                              pictures=pictures,
                              characteristics_detailed=total
                              )









        # loader=ItemLoader(item=LeroymerlenItem, response=response)
        # loader.add_xpath('article_number',"//uc-pdp-card-ga-enriched//span[contains(@slot,'article')]/text()")
        # loader.add_xpath('article_description',"//uc-pdp-card-ga-enriched//h1[contains(@slot,'title')]/text()")
        # loader.add_xpath('price',"//uc-pdp-price-view[1]//span[@slot='price']/text()")
        # loader.add_xpath('currency',"//uc-pdp-price-view[1]//span[@slot='currency']/text()")
        # loader.add_xpath('unit',"//uc-pdp-price-view[1]//span[@slot='unit']/text()")
        # loader.add_xpath('pictures',"//img[@slot='thumbs']/@src")
        # yield loader.load_item()



