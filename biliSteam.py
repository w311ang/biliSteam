import requests
import re
import pytools
import os
import pickle
import markdown
import time

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
  aid=one['aid']
  if not bvid in checked:
  #if True:
    des=requests.get('http://api.bilibili.com/x/web-interface/archive/desc?bvid=%s'%bvid).json()['data']
    try:
      link=des
    except AttributeError:
      link=requests.get('http://api.bilibili.com/x/v2/reply?type=1&oid=%s').json()['data']['upper']['top']['content']['message']
    link=re.search('(?<==\n)([\s\S]+)',des).group()
    link=link.replace('请相信我们的视频质量，值得你的关注！','')
    link=link.replace('\n','\n\n')
    bv=one['bvid']
    created=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(one['created']))
    umake.append({'title':one['title'],'des':des,'link':link,'bv':bv,'time':created})
    checked.append(bv)

#写邮件
for one in umake:
  title=one['title']
  link=one['link']
  bvlink='https://bilibili.com/video/'+one['bv']
  created=one['time']
  md+="""\
### %s
%s

%s

---
%s
"""%(title,created,bvlink,link)

with open('checked.txt','wb') as file:
  pickle.dump(checked,file)

content=markdown.markdown(md)
#print(md)
#print(checked)
#print(umake)
#umake=True
if umake:
  pytools.update(qpass=qpass,qfrom=qfrom)
  pytools.qmail('biliSteam',content,'Steam福利更新了',html=True)
else:
  print('无更新')
