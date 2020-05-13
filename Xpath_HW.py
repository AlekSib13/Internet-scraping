# 1)Написать приложение, которое собирает основные новости с сайтов news.mail.ru, lenta.ru, yandex.news
# Для парсинга использовать xpath. Структура данных должна содержать:
# название источника,
# наименование новости,
# ссылку на новость,
# дата публикации
#
# 2)Сложить все новости в БД

from lxml import html
from requests import get
import re
from pprint import pprint
from pymongo import MongoClient
import time
client=MongoClient('localhost',27017)
base=client.News

header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
dic = {}
###--Адресация между новостными источниками:
def source(news_source):
    if news_source=='mail':
        response=get('https://news.mail.ru/', headers=header)
        news_mail(response)
        time.sleep(3)
        second_major(response)
        time.sleep(3)
        extra_news(response)
    elif news_source=='lenta':
        response=get('https://lenta.ru/',headers=header)
        news_mail(response)
        time.sleep(3)
        second_major(response)
        time.sleep(3)
        extra_news(response)
    elif news_source=='yandex':
        response=get('https://yandex.ru/news',headers=header)
        extra_news(response)
    else:
        print('Название сайта указано неверно')

#---главная новость на странице, актуально для mail,lenta
def news_mail(response):
    root = html.fromstring(response.text)
    if news_source=='mail':
        main_news = root.xpath("//td[@class='daynews__main']//span[contains(@class,'photo__title')]//text()")
        link=root.xpath("//a[@class='photo photo_full photo_scale js-topnews__item']/@href")
        return full_info(piece_of_news(link)[0],piece_of_news(link)[1],main_news[0],piece_of_news(link)[2],piece_of_news(link)[3])
    elif news_source=='lenta':
        main_news=root.xpath("//h2//text()")[1]
        link=root.xpath("//h2/a/@href")
        publication_date = root.xpath("//h2/a//time/@datetime")
        return full_info(piece_of_news(link)[0],piece_of_news(link)[1],main_news,piece_of_news(link)[2],publication_date[0])

#--- сбор названия источника, ссылки, даты публикации: в зависимости от сайт, собираеся один из параметров или все
def piece_of_news(link):
    if news_source=='mail':
        response_link= get('https://news.mail.ru/'+link[0], headers=header)
        aggreg_link='https://news.mail.ru/'+link[0]
        link_root=html.fromstring(response_link.text)
        try:
            source_name=link_root.xpath("//a[@class='link color_gray breadcrumbs__link']//span[@class='link__text']/text()")[0]
        except:
            source_name='-'
        try:
            source_link=link_root.xpath("//a[@class='link color_gray breadcrumbs__link']/@href")[0]
        except:
            source_link='-'
        try:
            publication_date=link_root.xpath("//span[@class='breadcrumbs__item']//text()")[0]
        except:
            publication_date='-'
        return aggreg_link,source_name,source_link,publication_date
    elif news_source=='lenta':
        aggreg_link = 'https://lenta.ru/' + link[0]
        source_name='lenta.ru'
        source_link=aggreg_link
        return aggreg_link,source_name,source_link
    else:
        response_link = get(link, headers=header)
        response_link=html.fromstring(response_link.text)
        source=response_link.xpath("//h1//span//a/text()")
        return source

#---список новостей второстепенного блока, актуально для mail,lenta
def second_major(response):
    root = html.fromstring(response.text)
    if news_source=='mail':
        sm_news=root.xpath("//td[@class='daynews__items']/div")
        i = 1
        for element in sm_news[:2]:
            name=element.xpath(f"//div[position()={i}]/a[@class='photo photo_small photo_scale photo_full js-topnews__item']//text()")
            link=element.xpath(f"//div[position()={i}]/a[@class='photo photo_small photo_scale photo_full js-topnews__item']//@href")
            # piece_of_news(link)
            full_info(piece_of_news(link)[0],piece_of_news(link)[1],name[0],piece_of_news(link)[2],piece_of_news(link)[3])
            i+=1
    elif news_source=='lenta':
        for i in range(2,4):
            name = root.xpath(f"//section[contains(@class,'js-top-seven')]/div[@class='span4'][1]/div[position()={i}]//text()")
            publication_date = root.xpath(f"//section[contains(@class,'js-top-seven')]/div[@class='span4'][1]/div[position()={i}]//@datetime")
            link=root.xpath(f"//section[contains(@class,'js-top-seven')]/div[@class='span4'][1]/div[position()={i}]/a/@href")
            full_info(piece_of_news(link)[0],piece_of_news(link)[1],name[1],piece_of_news(link)[0],publication_date[0])


#---список остальных новостей. В отличие от mail и lenta, для yandex в данном блоке собирается почти полная информация по новости
def extra_news(response):
    root = html.fromstring(response.text)
    if news_source=='mail':
        li_news=root.xpath("//ul[@class='list list_type_square list_half js-module']/li")
        i = 1
        for element in li_news[:6]:
            name=element.xpath(f"//li[position()={i}]/a[@class='list__text']/text()")
            link=element.xpath(f"//li[position()={i}]/a[@class='list__text']/@href")
            piece_of_news(link)
            full_info(piece_of_news(link)[0],piece_of_news(link)[1],name[0],piece_of_news(link)[2],piece_of_news(link)[3])
            i+=1
    elif news_source=='lenta':
        for i in range(1,8):
            name = root.xpath(f"//section[contains(@class,'js-top-seven')]/div[@class='span4'][2]/div[position()={i}]//text()")
            publication_date = root.xpath(f"//section[contains(@class,'js-top-seven')]/div[@class='span4'][2]/div[position()={i}]//@datetime")
            link=root.xpath(f"//section[contains(@class,'js-top-seven')]/div[@class='span4'][2]/div[position()={i}]/a/@href")
            full_info(piece_of_news(link)[0],piece_of_news(link)[1],name[1],piece_of_news(link)[0],publication_date[0])
    else:
        tags=["//div[@aria-labelledby='Moscow_and_Moscow_Oblast']//tr","//div[@aria-labelledby='politics']//tr"]
        for tag in tags:
            li_news=root.xpath(f"{tag}")
            for element in li_news:
                items=element.xpath(".//td")
                for item in items:
                    name=item.xpath(".//div[@class='story__topic']//h2//text()")
                    source=item.xpath(".//div[@class='story__info']/div/text()")
                    publication_date=re.findall('\d+',str(item.xpath(".//div[@class='story__info']/div/text()")))
                    publication_date=':'.join(publication_date)
                    link=item.xpath(".//div[@class='story__topic']//a//@href")
                    link='https://yandex.ru'+link[0]
                    full_info(link,piece_of_news(link)[0],name[0],link,publication_date)


#--Полная информация о новости передается в словарь:
def full_info(aggreg_link,source_name,name,reference,date):
    dic['_id']=aggreg_link
    dic['Источник']=source_name
    dic['Название новости']=name
    dic['Ссылка на новость']=reference
    dic['Дата публикации']=date
    pprint(dic)
    return to_mongo(dic)


#--складываем в базу
def to_mongo(info):
    if news_source=='mail':
        collection=base['Mail.ru']
        collection.insert_one(dic)
    elif news_source == 'lenta':
        collection=base['Lenta.ru']
        collection.insert_one(dic)
    else:
         collection=base['Yandex.news']
         collection.insert_one(dic)



news_source=input('Введите название новостного сайта lenta/yandex/mail: ')
source(news_source)



