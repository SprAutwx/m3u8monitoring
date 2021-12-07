from  zhibojiancemoudle import ddmsgsend,ddmsgsendat
import re,requests,time,threading,random,os

f1 = open('/home/py/checkstream/nhls1.txt', 'r+', encoding="utf-8")
f1.truncate(0)
f1.close()

with open('/home/py/checkstream/nhls1.txt', 'a') as fe:
    stream = 'STREAM' + '\n'
    fe.write(stream)
    fe.close()
    
def duanliujiance(m3u8_url):
    response = requests.get(m3u8_url)
    HTTP_CODE = response.status_code
    if HTTP_CODE != 200:
        with open("waring.txt", 'a', encoding='utf-8')as war:
            wcode = str(HTTP_CODE)
            w = "M3U8访问异常，请检查：" + m3u8_url + "状态码：" + wcode + '\n'
            print(w)
            ddmsgsend(w)
            war.write(w)
            war.close()
    else:
        mmm = str(response.content)
        aaa = re.findall("#EXT-X-MEDIA-SEQUENCE:(.*?)\#", mmm)[0]
        time.sleep(30)
        response2 = requests.get(m3u8_url)
        mmm2 = str(response2.content)
        aaa2 = re.findall("#EXT-X-MEDIA-SEQUENCE:(.*?)\#", mmm2)[0]
        if aaa == aaa2:
            w = "连续两次请求M3U8参数相同，疑似断流:" + m3u8_url + '\n'
            print(w)
            ddmsgsendat(w)
            a1 = []
            a1.append(m3u8_url)
            t = threading.Thread(target=duanliuhuifu, args=(a1))
            t.start()
        else:
            with open('/home/py/checkstream/neiwanghls1.txt', 'a') as fe:
                urlstr = str(m3u8_url)
                if "0.0.0.11" in urlstr:
                    newurl = urlstr.replace("0.0.0.11" , 'host', )
                elif "0.0.0.12" in urlstr:
                    newurl =urlstr.replace("0.0.0.12", 'host', )
                elif "0.0.0.13" in urlstr:
                    newurl =urlstr.replace("0.0.0.13", 'host', )
                elif "0.0.0.51" in urlstr:
                    newurl =urlstr.replace("0.0.0.51", 'host', )
                elif "0.0.0.52" in urlstr:
                    newurl =urlstr.replace("0.0.0.52", 'host', )
                fe.write(newurl)
                fe.close()
                os.system("\cp /home/py/checkstream/neiwanghls1.txt /home/py/checkstream/neiwanghls.txt")

def duanliuhuifu(url):
    i = 1
    while i < 61 :
        response = requests.get(url)
        m1 = str(response.content)
        a1 = re.findall("#EXT-X-MEDIA-SEQUENCE:(.*?)\#", m1)[0]
        time.sleep(30)
        response2 = requests.get(url)
        m2 = str(response2.content)
        a2 = re.findall("#EXT-X-MEDIA-SEQUENCE:(.*?)\#", m2)[0]
        i = i + 1
        if a1 == a2:
            if i == 20:
                w = "断流尚未恢复:" + url + '\n'
                print(w)
                ddmsgsend(w)
                time.sleep(40)
                continue
            elif i == 60:
                w = "断流一小时未恢复，当天不再告警:" + url + '\n'
                print(w)
                ddmsgsend(w)
                break

        elif a1 != a2:
            w = "断流直播地址已经恢复:" + url + '\n'
            print(w)
            ddmsgsend(w)
            with open('/home/py/checkstream/neiwanghls.txt','a',encoding='utf-8') as f:
                urlstr = str(url)
                if "0.0.0.11" in urlstr:
                    newurl = urlstr.replace("0.0.0.11" , 'host', )
                elif "0.0.0.12" in urlstr:
                    newurl =urlstr.replace("0.0.0.12", 'host', )
                elif "0.0.0.13" in urlstr:
                    newurl =urlstr.replace("0.0.0.13", 'host', )
                elif "0.0.0.51" in urlstr:
                    newurl =urlstr.replace("0.0.0.51", 'host', )
                elif "0.0.0.52" in urlstr:
                    newurl =urlstr.replace("0.0.0.52", 'host', )                  
                f.write(newurl)
                f.close()
            break

with open('/home/py/checkstream/neiwanghls.txt','r') as fn:
    line = fn.readline()
    lock = threading.Lock()
    if lock.acquire():
        for line in fn:
            line.strip()
            hostlist = ['0.0.0.11', '0.0.0.12', '0.0.0.13','0.0.0.51','0.0.0.52']
            host = random.choice(hostlist)
            line = line.replace('host', host)
            a1 = []
            a1.append(line)
            t = threading.Thread(target=duanliujiance, args=(a1))
            t.start()
        lock.release()
fn.close()
