import http.server
import threading
import socket
import random
import zipfile
import time
import os
import sys
import psutil
import re
import platform
import asyncio
from . import cameraSocket
currentOs = platform.system()

'''
Date: 2024-02-21 18:15:26
author: zjs
description: 校验端口是否被占用
'''


def checkPort(port, host='localhost'):
    s = socket.socket()
    try:
        s.connect((host, port))
        return True
    except Exception as e:
        e
        return False
    finally:
        s.close()


'''
Date: 2024-02-21 18:24:21
author: zjs
description: 随机生成一个端口
'''


def randomPort():
    port = random.randint(10000, 49000)
    return port if not checkPort(port) else randomPort()


'''
Date: 2024-02-21 18:02:48
author: zjs
description: 创建静态资源服务器的线程内部方法
'''


def __creatStaticServer(CUSTOM_DIRECTORY):
    # 指定静态文件目录
    DIRECTORY = CUSTOM_DIRECTORY if CUSTOM_DIRECTORY else './'

    class CustomHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=DIRECTORY, **kwargs)

    PORT = randomPort()
    HOST = "127.0.0.1"
    # 直接启动服务器
    with http.server.HTTPServer((HOST, PORT), CustomHandler) as server:
        print(f"静态资源资源服务器启动在http://{HOST}:{PORT}, 资源路径为{DIRECTORY}")
        server.serve_forever()


'''
Date: 2024-02-21 18:02:48
author: zjs
description: 创建静态资源服务器
'''


def creatStaticServer(path=None):
    threading.Thread(target=__creatStaticServer, args=(path,)).start()


'''
Date: 2024-02-21 18:36:13
author: zjs
description: 指定路径生成zip
'''


def genZipByDirOrFile(path, name=str(time.time())+'.zip'):
    if not os.path.exists(path):
        return print('文件不存在')
    zipObj = zipfile.ZipFile(name, 'w')
    zipObj.write(path, compress_type=zipfile.ZIP_DEFLATED)
    zipObj.close()
    return name


'''
Date: 2024-02-23 11:42:47
author: zjs
description: 包装发送数据包
'''


def genSendPack(cmd, subcmd, data=None, uuid=[27, 27]):
    data = subcmd if data == None else data
    isStr = type(data) is str
    dataLen = len(data) if isStr else 0x01
    packLen = dataLen + 3
    head = [0x7e, 0x7e]
    end = [0xee, 0xee]
    result = head+[packLen, cmd, subcmd,
                   dataLen]
    if isStr:
        result = list(bytes(result) + data.encode())
    else:
        result = result + [data]
    result = result + uuid + end
    return bytes(result)


'''
Date: 2024-01-11 19:16:55
author: zjs
description: 获取终端参数
'''


def getArg(key='---cameraSokectPort'):
    for i, arg in enumerate(sys.argv):
        if (arg.startswith(key)):
            port = arg.split('=')
            return port[1]



'''
Date: 2024-03-26 16:55:17
author: zjs
description: 获取本机ip
'''
def getCurrentIp():
    s = None
    ip = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        if s is not None:
            s.close()

    return ip


'''
Date: 2024-03-26 16:55:17
author: zjs
description: 获取内网ip.用于绑定 udp
'''


def getHostIp():
    if currentOs == 'Windows':
        return getCurrentIp()
    elif currentOs == 'Darwin':
        return '0.0.0.0'


'''
Date: 2024-01-11 19:16:55
author: zjs
description: 根据端口 杀死本ip进程
'''


def killByPort(port):
    if not port:
        print('端口不存在')
        return

    if currentOs == 'Windows':
        filterVal = filter(lambda el: el.laddr.port == port and el.status in [
                           'LISTEN', 'NONE'] and el.laddr.ip == getHostIp(), psutil.net_connections())
        filterVal = list(filterVal)
        if len(filterVal):
            # ip + 端口 最多只能有一个
            activeProcessPid = filterVal[0].pid
            process = psutil.Process(activeProcessPid)
            process.terminate()
            return True

    elif currentOs == 'Darwin':
        result = (os.popen(f'lsof -i:{port}')).read()
        res = re.compile(r'\n.*? (\d+) ').findall(result)
        # 杀死所有进程
        for pid in res:
            # 占用端口的pid
            os.popen(f'kill -9 {pid}')


'''
Date: 2024-01-11 19:16:55
author: zjs
description:  获取uuid
'''


def genUuid():
    uuidNum = random.randrange(1, 65535)
    return [uuidNum - (uuidNum >> 8 << 8), uuidNum >> 8]


'''
Date: 2024-01-11 19:16:55
author: zjs
description:  防抖
'''


class setTimeOut:
    _timer = threading.Timer

    def __init__(self, fn, delay, args=None, kwargs=None) -> None:
        self._timer = threading.Timer(delay, fn, args, kwargs)
        self._timer.start()

    def clear(self):
        self._timer.cancel()


class debounce:
    timer: setTimeOut = None

    def __init__(self, func, delay) -> None:
        self.func = func
        self.delay = delay

    def __call__(self, *args, **kwargs):
        if self.timer is not None:
            self.timer.clear()
        self.timer = setTimeOut(self.func, self.delay, args, kwargs)
