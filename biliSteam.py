import requests
import re
import pytools
import os
import pickle

vlist=requests.get('http://api.bilibili.com/x/space/arc/search?mid=518876755&pn=1&ps=10').json()['data']['list']['vlist']
checked=[]
qpass=os.getenv('qpass')
qfrom=os.getenv('qfrom')
umake=[]
content=''

with open('checked.txt','rb') as file:
  if os.stat('checked.txt').st_size>1:
    checked=pickle.load(file)

for one in vlist:
  bvid=one['bvid']
  if not bvid in checked:
    des=requests.get('http://api.bilibili.com/x/web-interface/archive/desc?bvid=%s'%bvid).json()['data']
    link=re.findall('(?:https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]',des)
    bv=one['bvid']
    umake.append({'title':one['title'],'des':des,'link':link,'bv':bv})
    checked.append(bv)

#写邮件
for one in umake:
  title=one['title']
  link=one['link']
  bvlink='https://bilibili.com/video/'+one['bv']
  content+='=====%s=====\n'%title
  content+=bvlink+'\n'
  content+='----------\n'
  for alink in link:
    content+=alink+'\n'
  content+='\n'

with open('checked.txt','wb') as file:
  pickle.dump(checked,file)

print(content)
pytools.update(qpass=qpass,qfrom=qfrom)
pytools.qmail('biliSteam','快来白嫖Steam库！',content)
