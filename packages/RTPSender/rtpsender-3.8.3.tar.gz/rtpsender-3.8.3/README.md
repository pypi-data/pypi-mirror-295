## description
功能：将音视频数据转换成rtp包

## usage examples
安装av库
```bash
pip uninstall av && pip install av --no-binary av
```

提供了四个转换函数，支持传入原始文件和字节数据两种方式，具体使用方式请参考下面的示例：
```python

from pydub import AudioSegment
import cv2
from time import sleep, time

if __name__ == '__main__':
    ip_address = "10.253.101.36"
    # ip_address = "127.0.0.1"
    port = 7777
    image_file = "/Users/a58/Code/python/rtp/images/frame_0.png"
    image_files = ["/Users/a58/Code/python/rtp/images/frame_%d.png" % i for i in range(5)]
    audio_file = "/Users/a58/Code/python/rtp/audios/bgroup.wav"
    audio_16k_file = "/Users/a58/Code/python/rtp/audios/bgroup16k.wav"

    frame_size = (1080, 1920) # (width, height)

    rtpSender = RTPSender(ip_address, port, frame_size, hard_encode=False, open_log=True, days=7)
    rtpSender.stop()
    
    rtpSender = RTPSender(ip_address, port, frame_size, hard_encode=False, open_log=True, days=7)

    audio = AudioSegment.from_file(audio_16k_file, format="wav")
    audio_data = audio.raw_data
    i = 0
    cnt = 0
    t1 = time()

    init_cnt = 2

    imgs = [cv2.imread(image_file) for image_file in image_files]

    frame_cnt = 0

    while True:
        for img in imgs:
            if i >= len(audio_data) - 640:
                i = 0
            for j in range(25):
                # print("time: ", time())
                rtpSender.send_video_rtp_from_img(img)
                # rtpSender.send_video_rtp_from_img(img)
                # if packets_len > 0:
                #     print("packets_len: ", packets_len, ", frame_cnt: ", frame_cnt)
                frame_cnt += 1
                rtpSender.send_audio_rtp_from_bytes(audio_data[i:i+640], True)
                i += 640
                rtpSender.send_audio_rtp_from_bytes(audio_data[i:i+640], True)
                cnt += 1
                i += 640
                t2 = time()
                t = t1 + cnt*0.04 - t2
                # print("t: ", t)
                if t > 0:
                    # print("sleep: ", t)
                    sleep(t)
            # img = cv2.imread(image_file)
            # rtpSender.send_audio_rtp_from_file(audio_file)
            # t1 = time()
        if init_cnt < 20:
            rtpSender.stop()
            rtpSender = RTPSender(ip_address, port, frame_size, hard_encode=False, open_log=True, days=7)
            init_cnt += 1
            print("reinit rtpSender: ", init_cnt)

    # 只支持采样率48000HZ，单通道 20ms
    # rtpSender.send_audio_rtp_from_file(audio_file)
    # img = cv2.imread(image_file)
    # rtpSender.send_video_rtp_from_img(img)

    # audio = AudioSegment.from_file(audio_file, format="wav")
    # audio_data = audio.raw_data
    # # 只支持采样率48000HZ，单通道 20ms
    # rtpSender.send_audio_rtp_from_bytes(audio_data)
```