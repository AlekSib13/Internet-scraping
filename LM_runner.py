from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leroymerlen import settings
from leroymerlen.spiders.LM import LmSpider

if __name__=='__main__':
    crawler_settings=Settings()
    crawler_settings.setmodule(settings)

    query=input('Введите название товара: ')
    process=CrawlerProcess(settings=crawler_settings)
    process.crawl(LmSpider,search=query)
    process.start()