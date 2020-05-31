

#Домашнее задание
# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, записывающую собранные вакансии в созданную БД.
# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы.
# 3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.



#--- Парсинг и запись вакансий в ДБ Mongo (В том числе с учетом перезаписи повторяющихся по id вакансий)
from bs4 import BeautifulSoup as bs
from requests import get
from pprint import pprint
import re
from pymongo import MongoClient
import transliterate
client=MongoClient('localhost',27017)
db=client['Вакансии']
dic={}
header={'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
site=None
while True:
    site = input('Введите сайт:')
    if site=='sj' or site=='hh':
        vacancy=input('Введите название вакансии:')
        break

#--Переход на сайт с обозначенной вакансией
def job(site,vacancy):
    if site=='sj':
        link='https://www.superjob.ru/vacancy/search/?keywords='
        response=get(link+vacancy,headers=header).text
        soup=bs(response,'lxml')
        page_parse(soup)
    else:
        pass



def page_parse(soup):
    vacancies=soup.find('div',{'style':'display:block'})
    for element in vacancies:
        try:
            name=element.find('div',{'class':'jNMYr GPKTZ _1tH7S'}).find('a').getText()
            vacancy_link=element.find('div',{'class':'jNMYr GPKTZ _1tH7S'}).find('a')
            vacancy_link='https://www.superjob.ru'+vacancy_link['href']
            vacancy_description(vacancy_link,name,vacancy_parse(vacancy_link)[0],vacancy_parse(vacancy_link)[1],vacancy_parse(vacancy_link)[2],vacancy_parse(vacancy_link)[3],vacancy_parse(vacancy_link)[4],'-','-',vacancy_parse(vacancy_link)[5],vacancy_link)
        except:
            '-'
    next_page(soup)

def next_page(switch_page):
        try:
            next=switch_page.find(attrs='icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe')
            new_link='https://www.superjob.ru'+next['href']
            response=get(new_link,headers=header).text
            new_page=bs(response,'lxml')
            page_parse(new_page)
        except:
            '-'


def vacancy_parse(vacancy_link):
    root=get(vacancy_link,headers=header).text
    info=bs(root,'lxml')
    experience=info.find('div',{'class':'f-test-address _3AQrx'}).next_sibling()[0].getText()
    salary =info.find(attrs='_3mfro _2Wp8I ZON4b PlM3e _2JVkc').getText()
    company_name=info.find(attrs='_3zucV undefined').getText()
    location=info.find(attrs='_3mfro _1hP6a _2JVkc').getText()
    return experience,company_name,detailed_salary(salary)[0],detailed_salary(salary)[1],detailed_salary(salary)[2],location

def detailed_salary(info):
    info=str(info).replace('\xa0',' ')
    # salary_from=None
    # salary_to=None
    # currency=None
    if re.findall('—',info):
        salary_from=re.findall('\d+',info)[0]+' '+re.findall('\d+',info)[1]
        salary_to=re.findall('\d+',info)[2]+' '+re.findall('\d+',info)[3]
        currency = re.findall('руб\.|usd|eur', info)[0]
        return salary_from, salary_to, currency
    elif re.findall('от',info):
        salary_from=re.findall('\d+',info)[0]+' '+re.findall('\d+',info)[1]
        salary_to='-'
        currency = re.findall('руб\.|usd|eur', info)[0]
        return salary_from, salary_to, currency
    elif re.findall('до',info):
        salary_from='-'
        salary_to=re.findall('\d+',info)[0]+' '+re.findall('\d+',info)[1]
        currency = re.findall('руб\.|usd|eur', info)[0]
        return salary_from, salary_to, currency
    elif re.findall('По договорённости',info):
        salary_from='По договорённости'
        salary_to='-'
        currency = '-'
        return salary_from, salary_to, currency
    else:
        salary_from='-'
        salary_to='-'
        currency = '-'
        return salary_from, salary_to, currency


def vacancy_description(identifier,name,experience,company,salary_from,salary_to,currency,description,criteria,situated,vacancy_link):
    dic['_id']=identifier
    dic['Вакансия']=name
    dic['Требование к опыту']=experience
    dic['Организация']=company
    # dic['З/П'] = salary
    dic['З/П от']=salary_from
    dic['З/П до']=salary_to
    dic['Валюта']=currency
    dic['Описание']=description
    dic['Требования']=criteria
    dic['Расположение']=situated
    dic['Ссылка']=vacancy_link
    store(dic)
    pprint(dic)

def store(vacancy_info):
    if site=='sj':
        collection=db.sj_vacancies
        try:
            collection.insert_one(vacancy_info)
        except:
            collection.replaceOne({'_id':{'$el':vacancy_info['_id']}},{vacancy_info})
    else:
        pass

job(site,vacancy)


#--- Поиск вакансий по ценовому диапазону
name,symbol,sum=input('Выберете название вакансии: ').split(',')
def search(name,symbol,sum):
    collection=db.sj_vacancies
    try:
        if symbol=='<':
            for vacancy in collection.find({'$and':[{'Вакансия':name},{'$or':[{'З/П от':{'$lt':sum}},{'З/П до':{'$lt':sum}}]},{'$and':[{'З/П от':{'$ne':'-'}},{'З/П до':{'$ne':'-'}}]}]}).sort('З/П от'):
                print(vacancy)
        elif symbol == '<=':
            for vacancy in collection.find({'$and':[{'Вакансия':name},{'$or':[{'З/П от':{'$lte':sum}},{'З/П до':{'$lte':sum}}]},{'$and':[{'З/П от':{'$ne':'-'}},{'З/П до':{'$ne':'-'}}]}]}).sort('З/П от'):
                print(vacancy)
        elif symbol == '>':
            for vacancy in collection.find({'$and':[{'Вакансия':name},{'$or':[{'З/П от':{'$gt':sum}},{'З/П до':{'$gt':sum}}]},{'$and':[{'З/П от':{'$ne':'-'}},{'З/П до':{'$ne':'-'}}]}]}).sort('З/П от'):
                print(vacancy)
        elif symbol == '>=':
            for vacancy in collection.find({'$and':[{'Вакансия':name},{'$or':[{'З/П от':{'$gte':sum}},{'З/П до':{'$gte':sum}}]},{'$and':[{'З/П от':{'$ne':'-'}},{'З/П до':{'$ne':'-'}}]}]}).sort('З/П от'):
                print(vacancy)
        else:
            for vacancy in collection.find({'$and':[{'Вакансия':name},{'$or':[{'З/П от':{'$eq':sum}},{'З/П до':{'$eq':sum}}]},{'$and':[{'З/П от':{'$ne':'-'}},{'З/П до':{'$ne':'-'}}]}]}).sort('З/П от'):
                print(vacancy)
    except:
        '-'


search(name,symbol,sum)

