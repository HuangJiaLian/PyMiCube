import platform
import asyncio
from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError
import time
import signal

# 按键中断来控制结束信号 Ctrl + C
# 结束信号是为了让程序合理结束
END = False
def sigint_handler(signum, frame):
    global END
    END = True
    print ('Interrupted!')
signal.signal(signal.SIGINT, sigint_handler)

# 魔方地址
ble_address = (
    "D8:99:3A:4A:9E:8D"
    if platform.system() != "Darwin"
    else "9A8BE917-31DE-C67E-48C4-E9D833A6F0ED"
)

# 接收数据服务UUID
receive_UUID = "0000aadc-0000-1000-8000-00805f9b34fb"

pre_value = -1 # 上一次的数据
value = -1 # 这一次的数据

# 接收到魔方发出的数据就会进入这个中断函数
# 中断函数只做一件事，更新全局变量value的值
def notification_handler(sender, data):
    global value
    value = data

# 主要函数
async def main(ble_address, char_uuid):
    # 连接魔方
    device = await BleakScanner.find_device_by_address(ble_address, timeout=20.0)
    if not device:
        raise BleakError(f"A device with address {ble_address} could not be found.")
    
    async with BleakClient(device) as client:
        global value, pre_value
        print('Mi Smart Magic Cube connected.')
        # 注册消息中断函数: 有中断数据则执行函数 notification_handler
        await client.start_notify(char_uuid, notification_handler)
        while True:
            # 若value的值在中断函数中被更新则做相应的处理
            if value != pre_value:
                pre_value = value
                print(value, type(value)) 
                print(list(value))
            # 否则就睡觉
            else:
                await asyncio.sleep(0.1)
            
            # 接收到按键中断信号(Ctrl + C)时
            # 跳出循环
            if END == True:
                break
        # 通知魔方不要发信号了
        await client.stop_notify(char_uuid)
# 运行主要函数
asyncio.run(main(ble_address, receive_UUID))
