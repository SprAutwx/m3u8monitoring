import requests
import time
import cv2
import re
import json
import requests,time
import threading

#-------------------钉钉告警模块-------------------
TOKEN = ""

# SECRET = ""
headers = {'Content-Type': 'application/json;charset=utf-8'}
atmobile_list = [""]

def ddmsgsend(text):
    '''
    钉钉告警模块，通过关键字验证发送告警信息
    '''

    # headers = {'Content-Type': 'application/json;charset=utf-8'}
    # atmobile_list = [
    #                     "#手机号，每次邮件会艾特此人",
    #                     ""
    #                 ],
    # 传输方式为文本
    json_text = {
        "msgtype": "text",
        # 艾特人的方式
        "at": {
            # 艾特人按手机艾特
            #"atMobiles": atmobile_list,
            "isAtAll": False
        },
        # 发送文本
        "text": {
            "content": text
        }
    }
    # 请求url
    return requests.post(TOKEN, json.dumps(json_text), headers=headers).content.decode("utf8")

def ddmsgsendat(text):
    '''
    带@的钉钉告警模块，通过关键字验证发送告警信息
    '''
    json_text = {
        "msgtype": "text",
        # 艾特人的方式
        "at": {
            # 艾特人按手机艾特
            "atMobiles": atmobile_list,
            "isAtAll": False
        },
        # 发送文本
        "text": {
            "content": text
        }
    }
    # 请求url
    return requests.post(TOKEN, json.dumps(json_text), headers=headers).content.decode("utf8")

#-------------------opencv2监测视频参数模块-------------------

def rtmpstate(video_path):
    '''
    视频编码监测模块；
    这里监测视频编码的数据
    包括帧率，画幅等，帧数为0判断为断流
    '''
    video_capture = cv2.VideoCapture(video_path)
    video_FourCC = int(video_capture.get(cv2.CAP_PROP_FOURCC))  # 视频编码
    video_width = int(video_capture.get(3))
    video_height = int(video_capture.get(4))
    video_size = (int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                  int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print("video size:{}".format(video_size))  # (540, 960)
    # 视频帧率
    video_fps = int(video_capture.get(5))
    print("video_fps:{}".format(video_fps))
    codec = video_FourCC
    # print ('codec is %x'%(codec))
    print ('codec is ' + chr(codec&0xFF) + chr((codec>>8)&0xFF) + chr((codec>>16)&0xFF) + chr((codec>>24)&0xFF))#转换进制
    if video_fps == 0:
        with open("/home/py/checkstream/waring.txt", 'a', encoding='utf-8')as wfps:
            w = "RTMP断流:" + video_path + '\n'
            print(w)
            wfps.write(w)
            wfps.close()

    elif video_fps < 21 or video_fps > 61 :
        with open("/home/py/checkstream/waring.txt", 'a', encoding='utf-8')as wfps:
            wwfps = str(video_fps)
            w = video_path + "视频帧率异常,帧数:"  + wwfps + '\n'
            print(w)
            wfps.write(w)
            wfps.close()
            a = []
            a.append(video_path)
            t = threading.Thread(target=cvfps,args= (a))
            t.start()
            # t.join()

    width = [1280,1920,0]
    height = [1080,720,540,360,0]
    if video_width not in width or video_height not in height:
        with open("/home/py/checkstream/waring.txt", 'a', encoding='utf-8')as whf:
            wwidth = str(video_width)
            wheight = str(video_height)
            whuafu = (wwidth + "x" + wheight )
            w = video_path + "非标准画幅"  + whuafu + '\n'
            print(w)
            whf.write(w)
            whf.close()
            a = []
            a.append(video_path)
            t = threading.Thread(target=cvhuafu,args= (a))
            t.start()
    else:
        print(video_width,video_height)

#-------------------HTTP直播质量监控模块----------------------

def m3u8curl(m3u8_url):
    '''
    HLS访问数据监测；
    检测直播流的状态，响应时间等，
    并调用多线程模块进行恢复提醒
    '''
    response = requests.get(m3u8_url)
    # a1 = []
    # a1.append(m3u8_url)
    # t = threading.Thread(target=m3u8duanliujiance, args=(a1))
    # t.start()
    HTTP_CODE = response.status_code
    if HTTP_CODE != 200:
        with open("/home/py/checkstream/waring.txt", 'a',encoding='utf-8')as war:
            wcode = str(HTTP_CODE)
            w ="M3U8访问异常，请检查：" + m3u8_url + "状态码：" + wcode + '\n'
            print(w)
            #ddmsgsend(w)
            war.write(w)
            war.close()
            a = []
            a.append(m3u8_url)
            t = threading.Thread(target=hlsstate,args= (a))
            t.start()
    else:
        print("状态正常：%s"%HTTP_CODE)
    t= response.elapsed.total_seconds()*1000
    if t > 2000:
        a = []
        a.append(m3u8_url)
        t = threading.Thread(target=hlselapsed, args=(a))
        t.start()
    else:
        print("连接时间：%s 毫秒" % t)

    with open('/home/py/checkstream/youku.m3u8', 'wb') as tempTs:
        tempTs.write(response.content)

    # 读取m3u8每行文本
    with open('/home/py/checkstream/youku.m3u8', 'r') as m3u8:
    #获取ts片的响应时间
        for line in m3u8:
            if ".ts" in line:
                ts1 = line
                u1 = m3u8_url[0:m3u8_url.rfind('/', 1) + 1]
                tsurl = u1 + ts1
                # print(tsurl)
                rsp = requests.get(tsurl)
                rsp_time = rsp.elapsed.total_seconds()*1000
                print("%s 响应时间：%s毫秒"%(tsurl,rsp_time))
                if rsp_time >3000:
                    with open("/home/py/checkstream/waring.txt", 'a',encoding='utf-8')as war:
                        wtime = str(rsp_time)
                        w = "TS响应慢" + tsurl + "响应时间" + wtime + '\n'
                        nowtime = time.asctime(time.localtime(time.time()))
                        print(w)
                        war.write(w)
                        war.write(nowtime)
                        war.close()
    m3u8.close()

#-------------------告警邮件模块-------------------
def send_mail(to_list, sub, content):
    '''
    邮件告警模块，通过发送邮件告警
    '''
    me = mail_user + "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEText(content)
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user, mail_pass)
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        return True
    except Exception as e:
        print
        str(e)
        return False

def cvrecovery(cvurl):
    '''
    通过再次对视频进行检测，确定是否状态恢复，并钉钉提醒
    '''
    time.sleep(10)
    video_capture = cv2.VideoCapture(cvurl)
    video_FourCC = int(video_capture.get(cv2.CAP_PROP_FOURCC))  # 视频编码
    video_width = int(video_capture.get(3))
    video_height = int(video_capture.get(4))
    video_size = (int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                  int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print("video size:{}".format(video_size))  # (540, 960)
    # 视频帧率
    video_fps = int(video_capture.get(5))
    print("video_fps:{}".format(video_fps))
    codec = video_FourCC
    # 进制转换，输出编码格式
    print ('codec is ' + chr(codec&0xFF) + chr((codec>>8)&0xFF) + chr((codec>>16)&0xFF) + chr((codec>>24)&0xFF))#转换进制

def cvfps(cvurl):
    '''
    通过再次对视频进行检测，确定是否状态恢复，并钉钉提醒
    '''
    i = 0
    while i <3:
        video_capture = cv2.VideoCapture(cvurl)
        fps = int(video_capture.get(5))
        if fps>20 and fps <61:
            rfps = str(fps)
            msg = "以下直播帧数恢复正常" + '\n' + cvurl + '帧数：' +  rfps + 'http'
            print(msg)
            ddmsgsend(msg)
            break
        else:
            time.sleep(300)
            i = i + 1

def cvhuafu(cvurl):
    '''
    通过再次对视频进行检测，确定是否状态恢复，并钉钉提醒
    '''
    i = 0
    while i < 3:
        video_capture = cv2.VideoCapture(cvurl)
        video_width = int(video_capture.get(3))
        video_height = int(video_capture.get(4))
        width = [1280,1920,960]
        height = [1080,720,540,360]
        if video_width in width and video_height in height:
            www = str(video_width)
            hhh = str(video_height)
            msg = "以下直播画幅恢复正常" + '\n' + cvurl + '帧数：' +  www + 'x' + hhh
            ddmsgsend(msg)
            break
        else:
            time.sleep(300)
            i = i + 1

def hlsstate(hlsurl):
    '''
    通过再次对视频进行检测，确定是否状态恢复，并钉钉提醒
    '''
    i = 0
    while i < 3:
        response = requests.get(hlsurl)
        HTTP_CODE = response.status_code
        if HTTP_CODE == 200 :
            msg = "以下直播状态恢复正常" + '\n' + hlsurl
            ddmsgsend(msg)
            break
        else:
            time.sleep(300)
            i = i + 1

def hlselapsed(hlsurl):
    time.sleep(20)
    response = requests.get(hlsurl)
    t = response.elapsed.total_seconds() * 1000
    if t > 300 :
        wtime = str(t)
        w = "一分钟内M3U8多次响应缓慢"+ hlsurl + "响应时间" + wtime + '\n'      
        ddmsgsend(w)
        with open("/home/py/checkstream/waring.txt", 'a',encoding='utf-8')as war:
            print(w)
            war.write(w)
            war.close()
            
        i = 0
        while i < 3:
            response = requests.get(hlsurl)
            t = response.elapsed.total_seconds() * 1000
            if t > 300 :
               i = i + 1
            else:
                msg = "以下直播响应时间恢复正常" + '\n' + hlsurl
                ddmsgsend(msg)
                break

def m3u8duanliujiance(m3u8_url):
    response = requests.get(m3u8_url)
    HTTP_CODE = response.status_code
    if HTTP_CODE != 200:
        with open("/home/py/checkstream/waring.txt", 'a',encoding='utf-8')as war:
            wcode = str(HTTP_CODE)
            w ="M3U8访问异常，请检查：" + m3u8_url + "状态码：" + wcode + '\n'
            print(w)
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
            ddmsgsend(w)
