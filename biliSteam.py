import requests
import re
import pytools
import os
import pickle
import markdown

vlist=requests.get('http://api.bilibili.com/x/space/arc/search?mid=518876755&pn=1&ps=10').json()['data']['list']['vlist']
checked=[]
qpass=os.getenv('qpass')
qfrom=os.getenv('qfrom')
umake=[]
content=''
md=''

with open('checked.txt','rb') as file:
  if os.stat('checked.txt').st_size>1:
    checked=pickle.load(file)

for one in vlist:
  bvid=one['bvid']
  if not bvid in checked:
    des=requests.get('http://api.bilibili.com/x/web-interface/archive/desc?bvid=%s'%bvid).json()['data']
    link=re.findall('(?:https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]',des)
    move='https://weidian.com/?userid=1025773260&wfr=mkt-item-detail&spider_token=7038'
    if move in link:
      link.remove(move)
    bv=one['bvid']
    umake.append({'title':one['title'],'des':des,'link':link,'bv':bv})
    checked.append(bv)

#写邮件
for one in umake:
  title=one['title']
  link=''
  bvlink='https://bilibili.com/video/'+one['bv']
  for alink in one['link']:
    link+='1. %s\n'%alink
  md+="""\
### %s
%s

---
%s\
"""%(title,bvlink,link)

with open('checked.txt','wb') as file:
  pickle.dump(checked,file)

content=markdown.markdown(md)
#print(md)
pytools.update(qpass=qpass,qfrom=qfrom)
pytools.qmail('biliSteam',content,'Steam福利更新了',html=True)
