# 1) Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы)
# с сайта superjob.ru и hh.ru. Приложение должно анализировать несколько страниц сайта(также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:
# *Наименование вакансии
# *Предлагаемую зарплату (отдельно мин. отдельно макс. и отдельно валюту)
# *Ссылку на саму вакансию
#
# *Сайт откуда собрана вакансия
# По своему желанию можно добавить еще работодателя и расположение.
# Данная структура должна быть одинаковая для вакансий с обоих сайтов.
# Общий результат можно вывести с помощью dataFrame через pandas.
#---------------

import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import re

#----------------------
header={'User-Agent':
         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
link_to_vacancy='https://hh.ru/vacancy/'
#----------------------

def search_vacancy(link, header):
    vacancy_info=[]
    while True:
        response = requests.get(link, headers=header).text
        soup=bs(response,'lxml')
        company_vacancies = soup.find_all('div',{'data-qa': ['vacancy-serp__vacancy','vacancy-serp__vacancy vacancy-serp__vacancy_premium']})
        for company in company_vacancies:
            try:
                company_name=company.find('a',{'data-qa':'vacancy-serp__vacancy-employer'}).getText()
            except:
                company_name='-'
            finally:
                vacancy_name=company.find('a').getText()
                salary=company.find('span',{'data-qa':'vacancy-serp__vacancy-compensation'})
                vacancy_link=re.findall(link_to_vacancy+'\d+',str(company.find(attrs={'data-qa':'vacancy-serp__vacancy-title'})))
                vacancy_info.append({'Название компании':company_name,'Название вакансии':vacancy_name,'З/П от':vacancy_wage(salary)[0],'З/П до':vacancy_wage(salary)[1],'Валюта':vacancy_wage(salary)[2],'Cсылка на вакансию':vacancy_link[0],'Вакансия с':'hh'})
        switching_link=str(soup.find('a',{'class':'bloko-button HH-Pager-Controls-Next HH-Pager-Control'}))
        try:
            soup.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'}).getText()
            switching_link = re.findall('/search.*\d+', str(switching_link))
            link = 'http://hh.ru' + switching_link[0]
            continue
        except AttributeError:
            return print(vacancy_info)


#---------------------------------------
def vacancy_wage(salary):
    pattern = '\d{2,}'
    salary_interval = re.findall(pattern, str(salary))
    try:
        first=salary_interval[0]+salary_interval[1]
    except:
        first=''
    try:
        second=salary_interval[2]+salary_interval[3]
    except:
        second=''
    try:
        currency = re.findall('руб.|USD', str(salary))[0]
    except:
        currency=''
    return first,second,currency
#----------------------------------------


#----------------------------------------
site, vacancy= input('Введите сайт(hh/sj) и вакансию, пример "hh,бухгалтер": ').split(',')
if site=='hh':
    link=f'https://hh.ru/search/vacancy?area=1&st=searchVacancy&text={vacancy}'
elif site=='sj':
    link=f'https://www.superjob.ru/vacancy/search/?keywords={vacancy}&geo%5Bt%5D%5B0%5D=4'
else:
    raise Exception('Введен неверный сайт')

search_vacancy(link,header)






