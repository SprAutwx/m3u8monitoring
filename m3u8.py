import sys
import requests
import hashlib,time
import pycurl



# def checkCdnFile(url):
#     """
#     检测一个segment
#     """
#     requestHeaders = {'User-Agent': 'Android'}
#     response = requests.get(url)
#
#     headers = response.headers
#
#     md5 = headers.get('ETag')
#     md5 = md5[1: (len(md5) - 1)]
#     md5 = md5.lower()
#
#     print("headerMd5:" + md5)
#
#     with open('temp.ts', 'wb') as tempTs:
#         tempTs.write(response.content)
#
#     with open('temp.ts', 'rb') as tempTs:
#         data = tempTs.read()
#         realMd5 = hashlib.md5(data).hexdigest()
#         print("realMd5:" + realMd5)
#         if (md5 == realMd5):
#             print("correct_segment")
#         else:
#             print("error_segment：" + url)
#             print("error_header_md5" + md5)
#             print("error_real_md5" + realMd5)
#             sys.exit(1)
#


# 根据url下载m3u8文件.当然也可以注释掉这个下载
m3u8_url = ''
response = requests.get(m3u8_url)


c = pycurl.Curl()
c.setopt(pycurl.VERBOSE,0)
c.setopt(pycurl.CONNECTTIMEOUT, 5)    #连接的等待时间，设置为0则不等待
c.setopt(pycurl.TIMEOUT, 5)           #请求超时时间
c.setopt(pycurl.NOPROGRESS, 0)        #是否屏蔽下载进度条，非0则屏蔽
c.setopt(pycurl.MAXREDIRS, 5)         #指定HTTP重定向的最大数
c.setopt(pycurl.FORBID_REUSE, 1)      #完成交互后强制断开连接，不重用
c.setopt(pycurl.FRESH_CONNECT,1)      #强制获取新的连接，即替代缓存中的连接
c.setopt(pycurl.DNS_CACHE_TIMEOUT,60) #设置保存DNS信息的时间，默认为120秒
c.setopt(pycurl.URL,m3u8_url )
indexfile = open("content.txt","wb")
c.setopt(pycurl.WRITEHEADER,indexfile)  #将返回的HTTP HEADER定向到indexfile文件
c.setopt(pycurl.WRITEDATA,indexfile)    #将返回的HTML内容定向到indexfile文件


c.perform()
connect_time =  c.getinfo(pycurl.CONNECT_TIME)
t = connect_time*1000
HTTP_CODE =  c.getinfo(pycurl.HTTP_CODE)

if HTTP_CODE != 200:
    print("!!!httpcode%s"%HTTP_CODE)
else:
    print("状态正常：%s"%HTTP_CODE)


if t > 100:
    time.sleep(5)
    c1 = pycurl.Curl()
    c1.setopt(pycurl.URL, m3u8_url)
    c1.perform()
    c1.setopt(pycurl.VERBOSE, 0)
    connect_time1 = c1.getinfo(pycurl.CONNECT_TIME)
    t1 = connect_time1 * 1000
    if t1 > 100:
        print("dddddddddddddddddd%s"%t1);
    else:
        print("连接时间：%s 毫秒" % t1)

else:
    print("连接时间：%s 毫秒"%t)



with open('youku.m3u8', 'wb') as tempTs:
    tempTs.write(response.content)

# 读取m3u8每行文本
with open('youku.m3u8', 'r') as m3u8:
    # segmentCount = 0
    # for line in m3u8:
    #     line = line.strip('\n')
    #     if line.startswith("http"):
    #         segmentCount += 1
    #         print('no:%d'%(segmentCount))
    #         checkCdnFile(line)
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

            if rsp_time >200:
                print(m3u8_url)
            # with open('ts.txt','a') as tst:
            #     tst.write(tsurl)
            #     tst.close()
m3u8.close()

