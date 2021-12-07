import cv2

def rtmpstate(video_path):
# video_path = ""

    video_capture = cv2.VideoCapture(video_path)
    video_FourCC = int(video_capture.get(cv2.CAP_PROP_FOURCC))  # 视频编码
    video_width = int(video_capture.get(3))
    video_height = int(video_capture.get(4))
    video_size = (int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                  int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print("video size:{}".format(video_size))  # (540, 960)
    # 视频总帧数
    # total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))  # 799
    # print("total_frame:{}".format(total_frames))

    # 视频帧率
    video_fps = int(video_capture.get(5))
    print("video_fps:{}".format(video_fps))
    # video_fps_1 = video_capture.get(cv2.CAP_PROP_FPS)  # 视频帧率30
    # print("video_fps_1:{}".format(video_fps_1))
    codec = video_FourCC
    # print ('codec is %x'%(codec))
    print ('codec is ' + chr(codec&0xFF) + chr((codec>>8)&0xFF) + chr((codec>>16)&0xFF) + chr((codec>>24)&0xFF))#转换进制
    if video_fps == 0:
        with open("waring.txt", 'a', encoding='utf-8')as wfps:
            w = "RTMP断流:" + video_path + '\n'
            wfps.write(w)
            wfps.close()

    elif video_fps < 21 or video_fps > 61 :
        with open("waring.txt", 'a', encoding='utf-8')as wfps:
            wwfps = str(video_fps)
            w = video_path + "视频帧率异常,帧数:"  + wwfps + '\n'
            wfps.write(w)
            wfps.close()

    width = [1280,1920,0]
    height = [1080,720,540,360,0]
    if video_width not in width or video_height not in height:
        with open("waring.txt", 'a', encoding='utf-8')as whf:
            wwidth = str(video_width)
            wheight = str(video_height)
            whuafu = (wwidth + "x" + wheight )
            w = video_path + "非标准画幅"  + whuafu + '\n'
            whf.write(w)
            whf.close()
    else:
        print(video_width,video_height)
