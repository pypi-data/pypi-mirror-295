'''
Date: 2024-02-18 15:37:29
author: zjs
'''
import websocket
import socket
import json
import struct
import time
import copy
from . import util
from . import udp
import threading
from contextlib import closing


clientlock = threading.RLock()
serverlock = threading.RLock()

# 摄像头业务 socket 端口号
CAMERA_WS_PORT = 55555

# 摄像头业务socket
cameraServiceSocket = None

# 客户端业务socket
clientServiceSocket = None

# 摄像头服务端是否连接
isServerConnect = False
# 摄像头客户端是否连接
isClientConnect = False

# socket 返回值 根据uuid
serviceSocketResult = {}
serverWaitUuidList = []

# 客户端socket 返回值 根据uuid
clientSocketResult = {}

# 发送客户端的方法名称枚举
__sendClientFnEnum = {
    'onSinUdp': 'onSinUdp',
    'innerAddress': 'innerAddress',
    'getCameraPhoto': 'getCameraPhoto',
    'savePhoto': 'savePhoto'
}

# 发送客户端不需要等待的方法名称枚举
__sendClientNotWaitFnEnum = {
    'modifyModelStart': 'modifyModelStart'
}

# 改成两个客户端 通讯代理
'''
Date: 2024-02-18 15:46:25
author: zjs
description:获取摄像头业务 sokect
'''


def runCameraSocket(cameraIp):
    if cameraIp is None:
        print('摄像头ip不存在 runCameraSocket')
        return
    global cameraServiceSocket, clientServiceSocket, isServerConnect, serverWaitUuidList
    if isServerConnect:
        print('摄像头服务端socket正在连接中')
        return
    setup = 0
    try:
        cameraServiceSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cameraServiceSocket.connect((cameraIp, CAMERA_WS_PORT))
        isServerConnect = True
        # 不要删除这个打印
        print('摄像头连接成功')
        while True:
            # print('准备收')
            setup = 0
            serverMsg = cameraServiceSocket.recv(1024)
            setup = 1
            # print(serverMsg,len(serverMsg), '摄像头 ===>>>   py   ===>>>  客户端',[serverMsg[-4],serverMsg[-3]])
            # print('收：',[serverMsg[-4],serverMsg[-3]],len(serverMsg),serverMsg)
            if len(serverMsg) > 4 and serverMsg[0] == 0x7e and serverMsg[1] == 0x7e:
                uuidNum = serverMsg[-4] | serverMsg[-3] << 8
                # print("收处理：",uuidNum, uuidNum in serverWaitUuidList)
                if uuidNum in serverWaitUuidList:
                    serverWaitUuidList.remove(uuidNum)
                    serviceSocketResult[uuidNum] = serverMsg
            setup = 2
            if clientServiceSocket:
                __sendLockByClient(serverMsg)
            # time.sleep(0.05)

    except Exception as e:
        isServerConnect = False
        cameraServiceSocket.close()
        udp.CAMERA_INFO == {
            "ip": None,
            "port": None,
        }
        print('py sokect 读写错误1', setup, e)


'''
Date: 2024-02-19 17:43:27
author: zjs
description:  启动 socket 接口(http) 服务
'''
isPy = util.getArg('---isPy')


def runSocketApi(sokectPort):
    global cameraServiceSocket, clientServiceSocket, isClientConnect, clientSocketResult
    if isClientConnect:
        print('摄像头客户端socket正在连接中')
        return
    with closing(websocket.create_connection(f'ws://127.0.0.1:{sokectPort}')) as cilentWs:
        clientServiceSocket = cilentWs
        if not isPy:
            __sendLockByClient(f'setClient')
        try:
            isClientConnect = True
            while True:
                # # 50ms接收数据
                clientMsg = cilentWs.recv()
                # time.sleep(0.05)
                if not clientMsg or len(clientMsg) == 0 or clientMsg == None or clientMsg == 'jump':
                    continue
                if not cameraServiceSocket:
                    continue
                # print(clientMsg, '客户端 ===>>>   py   ===>>>  摄像头',[clientMsg[-6:-5],clientMsg[-4:-3]])
                jsonResult = json.loads(clientMsg)
                key = jsonResult['key']
                value = None
                uuid = None
                uuidNum = None
                if 'value' in jsonResult:
                    value = jsonResult['value']
                if 'uuid' in jsonResult:
                    # print('发：',key,[jsonResult['uuid']])
                    uuid = jsonResult['uuid']
                    uuidNum = (int(uuid[0]) | (int(uuid[1]) << 8))
                config = {
                    'useMode': lambda val, uuid: async_use_mode(val, uuid),
                    'reTrain': lambda val, uuid: __reTrain(val, uuid),
                    'getRes': lambda val, uuid: async_get_res(uuid),
                    'getVersion': lambda val, uuid: async_get_version(uuid),
                    'saveHandRes': lambda val, uuid: __saveHandRes(val),
                    'saveClasslyRes': lambda val, uuid: __saveClasslyRes(val),
                    'saveCardRes': lambda val, uuid: __saveCardRes(val),
                    'saveCarCodeRes': lambda val, uuid: __saveCarCodeRes(val),
                }
                # 指定key 需要缓存信息
                filterKey = __sendClientFnEnum.values()
                if key in filterKey and uuidNum is not None and uuidNum:
                    clientSocketResult[uuidNum] = jsonResult

                if key in config:
                    config[key](value, uuid)
        except Exception as e:
            print('py sokect 读写错误2', e)
            udp.CAMERA_INFO == {
                "ip": None,
                "port": None,
            }
            isClientConnect = False
    print('重新连接了')
    return runSocketApi(sokectPort)


# 模型cmd
modeType = {
    'face_detect': 0x01,  # 人脸检测
    'traffic_sign': 0x02,  # 交通标志
    'qr_code': 0x03,  # 二维码
    'face_recognition': 0x05,  # 人脸识别
    'classify': 0x06,  # 分类
    'gesture': 0x07,  # 手势
    'car_number': 0x08,  # 车牌
    'trace': 0x09,  # 物体追踪
    'mockxxx': 0x0a,  # 空
}


'''
Date: 2024-02-22 11:58:38
author: zjs
description: 等待指定uuid 消息返回结果
'''


def waitServiceSocketResult(uuid):
    global serviceSocketResult
    startTime = time.time()
    speedTime = time.time()
    # print('结果：',serviceSocketResult,uuid,  uuid not in serviceSocketResult)
    # 等待结果
    while uuid not in serviceSocketResult and (time.time() - startTime) < 4:
        time.sleep(0.1)
        if (time.time() - speedTime) > 2:
            speedTime = time.time()
            print('与摄像头通讯中')
        pass
    if ((time.time() - startTime) > 4) or not serviceSocketResult[uuid]:
        print('=== 摄像头通讯超时 ===')
        serviceSocketResult[uuid] = None
        return

    activeSocketResult = copy.deepcopy(serviceSocketResult[uuid])
    del serviceSocketResult[uuid]
    if activeSocketResult[5] != 0x01 or activeSocketResult[4] != 0x04:
        print('摄像头协议解析失败', activeSocketResult[5],
              activeSocketResult[4], activeSocketResult)
    return activeSocketResult


'''
Date: 2024-04-25 18:07:54
author: zjs
description: 以锁定的方式发送服务端socket
'''


def __sendLockByServer(val):
    if not val or not cameraServiceSocket:
        return
    with serverlock:
        cameraServiceSocket.sendall(val)
        # time.sleep(0.05)


'''
Date: 2024-02-22 11:58:38
author: zjs
description: 设置算法使用
这里之前是说 py 要封装成一个单独的sdk
但是开发到后边摄像头不能独立运行手势模型  于是产品决定py sdk 和 客户端耦合在一起  客户端跑模型
现在流程改为不再直接和摄像头通讯  py 通知客户端 业务逻辑在客户端处理后 用异步处理结束后 返回给 py
这里也很无奈 由于摄像头不是推送结果的方式 所以一直要问
问的话 在他切换大一点的模型比如交通卡片的时候  如果py不去通知客户端 继续问的话 摄像头会阻塞并一股脑的全部返回回来 到时候客户端又会报错
摄像头的硬件不好说话  所以说  后边的维护者自求多福吧
'''


def use_mode(mode, uuidHex=None):
    if uuidHex is None:
        uuidHex = util.genUuid()
    if not any(el == mode for el in list(modeType.keys())):
        return print(f'没有 {mode} 模式')
    global serverWaitUuidList
    cmd = 0x01
    __sendClientWithFn(__sendClientNotWaitFnEnum['modifyModelStart'], mode)
    uuid = (uuidHex[0] | (uuidHex[1] << 8))
    serverWaitUuidList.append(uuid)
    __sendLockByServer(util.genSendPack(
        cmd=cmd, subcmd=modeType[mode], uuid=uuidHex))
    waitServiceSocketResult(uuid=uuid)


'''
Date: 2024-02-22 11:58:38
author: zjs
description: 设置算法使用 异步版本给js 用
'''


def async_use_mode(mode, uuid):
    if not any(el == mode for el in list(modeType.keys())):
        return print(f'没有 {mode} 模式')
    cmd = 0x01
    __sendLockByServer(util.genSendPack(
        cmd=cmd, subcmd=modeType[mode], uuid=uuid))


'''
Date: 2024-02-22 11:58:38
author: zjs
description: 重新训练模型
'''


def __reTrain(val, uuid):
    mode, url = val['mode'], val['url']
    if not any(el == mode for el in [
       'classify',
       'face_recognition'
       ]):
        return print(f'没有 {mode} 模式')
    cmd = 0x02
    __sendLockByServer(
        util.genSendPack(cmd=cmd, subcmd=modeType[mode], data=url, uuid=uuid))


resultType = {
    'result': 0x00,  # 结果
    'version': 0x01,  # 版本号
    # '其他都是对应模型标签': 0x01,  # 标签
}

'''
Date: 2024-04-07 10:23:01
author: zjs
description: 存储手势结果
'''
__handRes = []


def __hand():
    global __handRes
    __handRes = []


resetHand = util.debounce(__hand, 0.35)


def __saveHandRes(val):
    global __handRes
    __handRes = []
    wristX = val[0][0]
    wristy = val[0][1]
    for i in val:
        tempList = i[0:-1]
        tempList[0] = round((tempList[0] - wristX)*10, 1)
        tempList[1] = round((tempList[1] - wristy)*10, 1)
        __handRes.append(tempList)
    # __handRes = [[
    #     0,
    #     0,
    #     0,
    #     0,
    #     val['conf'],
    #     val['name'],
    # ]]
    resetHand()


'''
Date: 2024-04-07 10:23:01
author: zjs
description: 存储分类结果
'''
__classlyRes = []


def __classly():
    global __classlyRes
    __classlyRes = []


resetClassly = util.debounce(__classly, 0.35)


def __saveClasslyRes(val):
    global __classlyRes
    __classlyRes = list(map(lambda el: [
        0,
        0,
        0,
        0,
        el['conf'],
        el['name'],
    ],val))
    resetClassly()


'''
Date: 2024-04-01 14:19:32
author: zjs
description: 卡片结果
'''

__cardRes = []


def __card():
    global __cardRes
    __cardRes = []


resetCard = util.debounce(__card, 0.35)


def __saveCardRes(val):
    global __cardRes
    __cardRes = [[
        val['x'],
        val['y'],
        val['width'],
        val['height'],
        val['conf'],
        val['name'],
    ]]
    resetCard()


'''
Date: 2024-04-01 14:19:32
author: zjs
description: 车牌结果
'''

__carCodeRes = []


def __carCode():
    global __carCodeRes
    __carCodeRes = []


resCarCode = util.debounce(__carCode, 0.35)


def __saveCarCodeRes(val):
    global __carCodeRes
    __carCodeRes = [[
        val['x'],
        val['y'],
        val['width'],
        val['height'],
        val['conf'],
        val['name'],
    ]]
    resCarCode()


'''
Date: 2024-04-01 14:19:32
author: zjs
description: 获取手势模型结果
'''


def __gestureModelResult(__):
    if not cameraServiceSocket:
        print('摄像头未连接请稍后')
    return __handRes


'''
Date: 2024-04-01 14:19:32
author: zjs
description: 获取卡片模型结果
'''


def __y8CardModelResult(__):
    if not cameraServiceSocket:
        print('摄像头未连接请稍后')
    return __cardRes

'''
Date: 2024-04-01 14:19:32
author: zjs
description: 获取分类模型结果
'''


def __classlyModelResult(__):
    if not cameraServiceSocket:
        print('摄像头未连接请稍后')
    if not len(__classlyRes):
        return None

    result = __classlyRes[0]
    for index in range(0, len(__classlyRes)):
        activeItem = __classlyRes[index]
        if float(activeItem[4]) > float(result[4]):
            result = activeItem
    return [result]


'''
Date: 2024-04-01 14:19:32
author: zjs
description: 获取车牌模型结果
'''


def __carCodeModelResult(__):
    if not cameraServiceSocket:
        print('摄像头未连接请稍后')
    return __carCodeRes


'''
Date: 2024-04-01 14:21:46
author: zjs
description: 获取基础模型返回值
'''


def __getBaseModelResult(hexList):
    resultLength = hexList[12]
    dateStartIndex = 16
    dateLength = 46

    resultData = hexList[dateStartIndex:dateStartIndex +
                         dateLength * resultLength]
    resultSlice = []
    # 分片获取结果
    for index in range(0, int(len(resultData) / dateLength)):
        activeChunk = resultData[index *
                                 dateLength: index * dateLength + dateLength]
        # 位置信息和返回值
        value = activeChunk[4: 4 + activeChunk[0]].decode('utf-8')
        leftTopY, rightBottomY, leftTopX, rightBottomX = [
            activeChunk[el] | (activeChunk[el + 1] << 8)
            for el in [34, 36, 38, 40]
        ]
        # 准确度
        confBytes = activeChunk[42:46]
        conf = struct.unpack('f', confBytes)[0]

        # 将浮点数转换为百分比，并保留两位小数
        conf = round(conf * 100, 2) or 0
        resultSlice.append([
            leftTopX,
            leftTopY,
            abs(rightBottomX - leftTopX),
            abs(rightBottomY - leftTopY),
            conf,
            value,
        ])
    return resultSlice


'''
Date: 2024-02-22 13:55:46
author: zjs
description: 获取识别结果 [x,y,w,h,p,result]
0x00 结果
0x01 标签
'''


def get_res(uuidHex=None):
    if uuidHex is None:
        uuidHex = util.genUuid()
    cmd = 0x03
    if not cameraServiceSocket:
        print('摄像头未连接')
    # print('发：',uuidHex)
    uuid = (uuidHex[0] | (uuidHex[1] << 8))
    serverWaitUuidList.append(uuid)
    __sendLockByServer(
        util.genSendPack(cmd=cmd, subcmd=resultType['result'], uuid=uuidHex))
    # print('等待：',uuidHex[0] | (uuidHex[1] << 8))
    hexList = waitServiceSocketResult(uuid=uuid)

    if hexList is None:
        return []
    if hexList[8] == modeType['gesture']:
        activeMethod = __gestureModelResult
    elif hexList[8] == modeType['traffic_sign'] or hexList[8] == modeType['trace']:
        activeMethod = __y8CardModelResult
    elif hexList[8] == modeType['car_number']:
        activeMethod = __carCodeModelResult
    elif hexList[8] == modeType['classify']:
        activeMethod = __classlyModelResult
    else:
        activeMethod = __getBaseModelResult

    res = activeMethod(hexList)

    if isinstance(res,list) and  res != [] and isinstance(res[0], list) :
        if hexList[8] == modeType['face_detect'] and len(res[0]) >=6:
            res=res[0][:4]
        elif hexList[8] == modeType['classify'] and len(res[0]) >=6:
            max=res[0]
            for i in res:
                if i[4]>max[4]:
                    max=i        
            res=max[5:]
        elif hexList[8] == modeType['qr_code'] and len(res[0]) >=6: 
            res=res[0][5:]  
        elif hexList[8] == modeType['gesture']:
            pass
        elif hexList[8] == modeType['traffic_sign'] :
                if len(res[0]) == 6:
                    del res[0][4]
                res=res[0]   
        else:
            if len(res[0]) >= 6:
                del res[0][4]
            res=res[0]   
    
    return res


'''
Date: 2024-02-22 13:55:46
author: zjs
description: 获取识别结果 [(x,y,w,h,p,result)]  异步版本给js用
0x00 结果
0x01 标签
'''


def async_get_res(uuid):
    cmd = 0x03
    if not cameraServiceSocket:
        print('摄像头未连接')
        return
    __sendLockByServer(
        util.genSendPack(cmd=cmd, subcmd=resultType['result'], uuid=uuid))


'''
Date: 2024-02-22 13:55:46
author: zjs
description: 获取摄像头版本号
0x01 版本号
'''


def async_get_version(uuid):
    cmd = 0x03
    if not cameraServiceSocket:
        print('摄像头未连接')
        return
    __sendLockByServer(
        util.genSendPack(cmd=cmd, subcmd=resultType['version'], uuid=uuid))


'''
Date: 2024-02-23 18:56:47
author: zjs
description: 获取人脸标签
'''


def get_face_tags():
    cmd = 0x03
    if not cameraServiceSocket:
        print('摄像头未连接')
        return
    __sendLockByServer(
        util.genSendPack(cmd, modeType['face_recognition']))


'''
Date: 2024-02-23 18:56:47
author: zjs
description: 获取分类标签
'''


def get_class_tags():
    cmd = 0x03
    if not cameraServiceSocket:
        print('摄像头未连接')
        return
    __sendLockByServer(
        util.genSendPack(cmd, modeType['classify']))


'''
Date: 2024-02-23 18:56:47
author: zjs
description: 获取当前模型标签
'''


def get_tags():
    return [el[-1] for el in get_res()]


'''
Date: 2024-02-22 17:41:35
author: zjs
description: 给客户端发送socket
'''


def __sendLockByClient(val):
    try:
        if not val or not clientServiceSocket:
            return
        with clientlock:
            activeMethod = clientServiceSocket.send if isinstance(
                val, str) else clientServiceSocket.send_bytes
            activeMethod(val)
            # time.sleep(0.05)
    except Exception as e:
        print(e, '__sendLockByClient error')


'''
Date: 2024-01-11 19:16:55
author: zjs
description: 通过 key val 格式消息给客户端
'''


def __sendClientWithFn(key, val=''):
    try:
        if not key:
            print('获取发送客户端标识符失败')
            return None
        uuidHex = util.genUuid()
        uuid = uuidHex[0] | (uuidHex[1] << 8)
        clientKey = f'__msg__{key}____{val}____{uuid}'
        __sendLockByClient(clientKey)
        return uuid
    except Exception as e:
        print(e, '__sendClientWithFn error')


'''
Date: 2024-01-11 19:16:55
author: zjs
description:  等待客户端消息回复
'''


def waitClientSocketResult(uuid):
    global clientSocketResult
    startTime = time.time()
    speedTime = time.time()
    # 等待结果
    while uuid not in clientSocketResult and (time.time() - startTime) < 8:
        time.sleep(0.1)
        if (time.time() - speedTime) > 2:
            speedTime = time.time()
            print('与客户端通讯中')
        pass

    if ((time.time() - startTime) > 8) or not clientSocketResult[uuid]:
        print('=== 客户端通讯超时 ===')
        return
    activeSocketResult = copy.deepcopy(clientSocketResult[uuid])
    del clientSocketResult[uuid]

    return activeSocketResult
