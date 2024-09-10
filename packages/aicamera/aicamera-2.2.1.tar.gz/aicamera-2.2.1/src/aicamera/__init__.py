# -*- coding: utf-8 -*-
'''
Date: 2024-02-19 17:28:41
author: zjs 15032985110
description: sdk 流程
1 引入后首先监听 udp 广播 直到发现目标 不发现目标以下没意义
2 获取摄像头 ip  根据ip 进行 rtsp拉流
3 根据ip 进行 业务socket连接(tcp)
4 暴露 socket 代理服务(中转对外是http  后边有时间可以加配置参数兼容tcp， 应用层直接tcp太麻烦)和 api 接口

使用方法：
1 python 引入sdk 引用对应api
2 其他服务通过 sokect 连接代理服务通讯  需要在脚本启动的时候加 --sokectPort=端口号 参数

举例：
import 依赖包 as sdk

# 初始化
sdk.init(arg?=)


初始化完毕后可以调用摄像头通讯
其中 __ 开头得函数代表暂时不对外暴露

version: 2.1.4

'''
import threading
import asyncio
import time
from . import udp
from . import util
from . import wifi
from . import lcd
from . import image
from . import rtsp
from . import cameraSocket
from .cameraSocket import get_res, use_mode, modeType, get_tags
from .image import take_photo, save


'''
Date: 2024-02-21 18:38:07
author: zjs
description: sdk 初始化方法 给py用
'''


def init(sin=None):
    # 开启接收广播线程
    serverThread = threading.Thread(target=udp.serverRun, args=(sin, True))
    serverThread.start()

    # # 开启发送广播线程
    # clientThread = threading.Thread(target=udp.cilentRun)
    # clientThread.start()

    # # 考虑后边是否需要多个客户端得时候干掉上一个进程
    # print(f'$$pid={os.getpid()}$$')
    while cameraSocket.cameraServiceSocket is None:
        if not sin:
            print('未指定设备编号')
        else:
            print('摄像头初始化中...')
        time.sleep(5)
        pass
    # 给用户需要简化流程 默认给他启动一个模型
    # use_mode('face_detect')
    # print('已切换到人脸检测模式')


'''
Date: 2024-02-21 18:38:07
author: zjs
description: sdk 异步初始化方法 给客户端js用
'''


def asyncInit(val=None):
    # 开启接收广播线程
    asyncServerThread = threading.Thread(target=udp.serverRun)
    asyncServerThread.start()


isPy = util.getArg('---isPy')
if isPy is None:
    asyncInit()
