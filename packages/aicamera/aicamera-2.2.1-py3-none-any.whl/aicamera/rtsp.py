import cv2
import time
from . import udp

# 缓存20-50帧
CAMERA_CACHE_LIST = []
# 上次流地址
RTSP_URL = None
'''
Date: 2024-02-18 15:22:12
author: zjs
description: 从摄像头读数据
'''
ACTIVE_CAMERA = None


async def read(cam):
    print(cam)
    global ACTIVE_CAMERA, RTSP_URL
    if ACTIVE_CAMERA and ACTIVE_CAMERA.isOpened() and RTSP_URL == cam:
        print('摄像头已经连接')
        return
    cap = cv2.VideoCapture(cam)
    RTSP_URL = cam
    ACTIVE_CAMERA = cap
    print('摄像头已经连接')
    while True:
        if cap.isOpened():
            try:
                isNew, frame = cap.read()
                if not isNew:
                    print("rtsp 已断开")
                    return
                frame = cv2.flip(cv2.transpose(frame), 0)
                # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                if len(CAMERA_CACHE_LIST) > 30:
                    del CAMERA_CACHE_LIST[:10]
                CAMERA_CACHE_LIST.append(frame)
                # cv2.imshow("frame", frame)
                # cv2.waitKey(1)
            # 获取视频流异常后重新拉取
            except Exception as e:
                print(e)
                cap = cv2.VideoCapture(cam)
                ACTIVE_CAMERA = cap
                time.sleep(2)
        else:
            print("拉取流地址失败")
            udp.CAMERA_ID = {
                "ip": None,
                "port": None,
            }
            return


'''
Date: 2024-02-18 15:22:12
author: zjs
description: 获取当前帧
'''


def getCurrentFrame():
    if not len(CAMERA_CACHE_LIST):
        return print('当前摄像头没有数据')
    return CAMERA_CACHE_LIST.pop()
