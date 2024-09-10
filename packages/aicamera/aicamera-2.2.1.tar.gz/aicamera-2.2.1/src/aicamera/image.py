import time
import os
import cv2
from . import cameraSocket

'''
Date: 2024-02-22 11:01:55
author: zjs
description: 从摄像头获取一张图片
'''


def take_photo():
    uuid = cameraSocket.__sendClientWithFn(
        cameraSocket.__sendClientFnEnum['getCameraPhoto'])
    if uuid is None:
        print('获取图片uuid失败')
        return
    result = cameraSocket.waitClientSocketResult(uuid)
    if result is not None and 'value' in result:
        return cv2.imread(result['value'])
    else:
        print('获取图片url失败')
        return


'''
Date: 2024-02-22 11:05:23
author: zjs
description: 保存图片
'''


def save(imaData, imgName=f'{int(time.time())}.jpg'):
    if imaData is None :
        print('图片数据不存在')
        return
    if imgName is None :
        imgName = f'{int(time.time())}.jpg'
    if not imgName.endswith('.jpg'):
        imgName += '.jpg'
    saveFile = os.path.normpath(os.path.join(os.getcwd(), imgName))
    # 没有路径创建路径
    saveDir = os.path.dirname(saveFile)
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)
    imaData = cv2.cvtColor(imaData, cv2.COLOR_BGR2RGB)
    cv2.imwrite(saveFile, imaData)
    cameraSocket.__sendClientWithFn(cameraSocket.__sendClientFnEnum['savePhoto'],saveFile)
    return imgName
