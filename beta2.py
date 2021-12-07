from zhibojiancemoudle import rtmpstate,m3u8curl,ddmsgsend,m3u8duanliujiance
import time,requests,re,threading,random

with open('/home/py/checkstream/hls.txt','r+') as f:
    line = f.readline()
    for line in f:
        cdnlist = ['test.com','test2.com']
        cdnname = random.choice(cdnlist)
        line = line.replace('cdn.test.com',cdnname)
        m3u8curl(line)
    f.close()

with open('/home/py/checkstream/waring.txt','a' ,encoding='utf-8') as ff:
    wtime = time.asctime(time.localtime(time.time()))
    ff.write(wtime)
    ff.close()

f1 = open('/home/py/checkstream/waring.txt', 'r+', encoding="utf-8")
msg = f1.read()
ddmsgsend(msg)
f1.truncate(0)
f1.close()
