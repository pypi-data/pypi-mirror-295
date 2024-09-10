
from .udp import CAMERA_INFO
from .util import checkPort

'''
Date: 2024-02-22 10:38:20
author: zjs
description: wifi 是否连接
'''


def is_connected():
    if not CAMERA_INFO['ip']:
        return False
    return checkPort(host=CAMERA_INFO['ip'], port=CAMERA_INFO['port'])


