import requests
import json
from pprint import pprint
link='http://api.musixmatch.com/ws/1.1/track.search'
header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
key={'apikey':'fb885e960dbb832c214a1d535ff14841',
     'q_track_artist':'EMINEM'}
r=requests.get(link,params=key,headers=header)
pprint(r.text)
with open('server_answer.json','w') as file:
    json.dump(r.text,file)