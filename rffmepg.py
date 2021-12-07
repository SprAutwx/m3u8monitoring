import ffmpeg
import sys
# 
# 
# # # 执行probe执行
# # probe = ffmpeg.probe(video_capture)
# # ffmpeg.input()
# # video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
# # if video_stream is None:
# #     print('No video stream found', file=sys.stderr)
# #     sys.exit(1)
# # # 宽度
# # width = int(video_stream['width'])
# # # 高度
# # height = int(video_stream['height'])
# # # 帧数
# # num_frames = int(video_stream['nb_frames'])
# # # 时长
# # time = (video_stream['duration'])
# # # 比特率
# # bitrate = (video_stream['bit_rate'])
# #
# # print('width: {}'.format(width))
# # print('height: {}'.format(height))
# # print('num_frames: {}'.format(num_frames))
# # print('time: {}'.format(time))
# # print('bitrate: {}'.format(bitrate))
# #
# # # 查看全部信息
# # print(video_stream)
# #
# 
def get_source_info_ffmpeg(source_name):
    return_value = 0
    try:
        info = ffmpeg.probe(source_name)
        # print(info)
        # print("---------------------------------")
        vs = next(c for c in info['streams'] if c['codec_type'] == 'video')
        format_name = info['format']['format_name']
        codec_name = vs['codec_name']
        duration_ts = float(vs['duration_ts'])
        fps = vs['r_frame_rate']
        width = vs['width']
        height = vs['height']
        print("format_name:{} \ncodec_name:{} \nduration_ts:{} \nwidth:{} \nheight:{} \nfps:{}".format(format_name, codec_name, duration_ts, width, height, fps))
    except (OSError, TypeError, ValueError, KeyError, SyntaxError) as e:
        print("init_source:{} error. {}\n".format(source_name, str(e)))
        return_value = 0
    return return_value

def main():
    source_name = str("")
    get_source_info_ffmpeg(source_name)

if __name__ == "__main__":
    main()
