# -*- coding: utf-8 -*-
import sys
import asyncio
import platform
import signal
import pyautogui

from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError

import numpy as np 

# 用按键中断来控制结束信号
END = False
def sigint_handler(signum, frame):
    global END
    END = True
    print ('Interrupted!')
signal.signal(signal.SIGINT, sigint_handler)

# 魔方的地址
ble_address = (
    "D8:99:3A:4A:9E:8D"
    if platform.system() != "Darwin"
    else "9A8BE917-31DE-C67E-48C4-E9D833A6F0ED"
)

# 这个UUID是用来接受数据用的
receive_UUID = "0000aadc-0000-1000-8000-00805f9b34fb"

# 这一串数据是用来解密收到的数据的
key = [176,  81, 104, 224,  86, 137,
       237, 119,  38,  26, 193, 161,
       210, 126, 150,  81,  93,  13,
       236, 249,  89, 235,  88,  24,
       113,  81, 214, 131, 130, 199,
         2, 169,  39, 165, 171, 41]

pre_value = -1
value = -1

# 将接收到的数据转换成十六进制的明文
def toHexVal(value, key):
    raw = list(value)
    k1 = raw[-1] >> 4 & 0xf
    k2 = raw[-1] & 0xf
    for i in range(18):
        raw[i] += key[i + k1] + key[i + k2]
    raw = raw[:18]

    valhex = []
    for i in range(len(raw)):
        valhex.append(raw[i] >> 4 & 0xf)
        valhex.append(raw[i]  & 0xf)
    return valhex

# 接收到魔方发出的数据就会进入这个中断函数
# 中断函数只做一件事，更新全局变量value的值
def notification_handler(sender, data):
    global value
    value = data


# 主函数
async def main(address, char_uuid):
    global value, pre_value, key, END
    device = await BleakScanner.find_device_by_address(address, timeout=30.0)
    if not device:
        raise BleakError(f"A device with address {ble_address} could not be found.")
    
    async with BleakClient(device) as client:
        print(f"Connected: {client.is_connected}")
        # 注册消息中断函数
        await client.start_notify(char_uuid, notification_handler)
        while True:
            # 若value的值在中断函数中被更新
            # 则做相应的处理
            if value != pre_value:
                pre_value = value
                valhex = toHexVal(value, key)
                print(valhex)
                anticlockwise = True if valhex[-3] == 3 else False

                # 蓝色面控制播放暂停
                if valhex[-4] == 1:
                    pyautogui.typewrite(' ')

                # 绿色面控制上下一首
                if valhex[-4] == 6:
                    if anticlockwise:
                        pyautogui.typewrite('[')
                    else:
                        pyautogui.typewrite(']')
            # 否则就睡觉
            else:
                await asyncio.sleep(0.1)
            # 接收到按键中断信号(Ctrl + C)时
            # 跳出循环
            if END == True:
                break
        # 通知魔方不要发数据? 
        await client.stop_notify(char_uuid)


if __name__ == "__main__":
    asyncio.run(main(ble_address,receive_UUID))

