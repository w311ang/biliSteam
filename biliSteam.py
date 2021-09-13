import requests
import re
import pytools
import os
import pickle
import markdown
import time
from random import choice

vlist=requests.get('http://api.bilibili.com/x/space/arc/search?mid=518876755&pn=1&ps=10').json()['data']['list']['vlist']
checked=[]
qpass=os.getenv('qpass')
qfrom=os.getenv('qfrom')
umake=[]
content=''
md=''
token=os.getenv('token')
message=['又有新游戏哦？','有抽奖吗，我来当分母','白嫖游戏啦','等待党的胜利！！！​','我在B站有套房[doge]​','给我给我给我给我给我给我给我给我给我给我给我给我给我给我[大笑][大笑][大笑][大笑][大笑][大笑][大笑][大笑][大笑][大笑][大笑][大笑][大笑]​']免费领取一款随机游戏[doge]​','[doge]哪有404.明明是打不开网址​']

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
      link=re.search('(?<==\n)([\s\S]+)',des).group()
    except AttributeError:
      top=requests.get('http://api.bilibili.com/x/v2/reply?type=1&oid=%s'%aid).json()['data']['upper']['top']['content']['message']
      link=re.search('(?<==\n)([\s\S]+)',top).group()
    link=link.replace('请相信我们的视频质量，值得你的关注！','')
    link=link.replace('\n','\n\n')
    bv=one['bvid']
    created=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(one['created']))

    with requests.post('http://api.bilibili.com/x/v2/reply/add',params={'access_key':token,'type':1,'oid':aid,'message':choice(message)}) as resp:
      json=resp.json()
      code=json['code']
      if code==0:
        comment='抽奖评论发送成功'
      else:
        comment='抽奖评论发送失败，错误码%s'%code

    umake.append({'title':one['title'],'des':des,'link':link,'bv':bv,'time':created,'comment':comment})
    checked.append(bv)
    time.sleep(60)

#写邮件
for one in umake:
  title=one['title']
  link=one['link']
  bvlink='https://bilibili.com/video/'+one['bv']
  created=one['time']
  comment=one['comment']
  md+="""\
### %s
%s

%s

%s

---
%s
"""%(title,created,bvlink,comment,link)

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
