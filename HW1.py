import requests
import json
from pprint import pprint
#link='https://api.github.com/users/'
#params={'AlekSib13'}
#header='Authorization: bearer 60410e48038a3be438d880147e1f489afb533d13" -X POST -d '
#q=requests.get(link,params)
#print(q.content)


name=input(f'Введите имя пользователя Github: ')
link=f'https://api.github.com/users/{name}/repos'
header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
q=requests.get(link,headers=header)
info=json.loads(q.text)
i=range(0,len(info))
with open ('repos.json','w',encoding='utf-8') as file:
    for i in info:
        json.dump(i['name'],file)
        file.write('\n')
