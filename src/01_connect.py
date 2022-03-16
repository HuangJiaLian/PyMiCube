import platform
import asyncio
from bleak import BleakClient, BleakScanner

# 魔方的地址, 不同系统呈现的地址不一样
# Windows和Linux是上面的格式， macOS是下面的格式
ble_address = (
    "D8:99:3A:4A:9E:8D"
    if platform.system() != "Darwin"
    else "9A8BE917-31DE-C67E-48C4-E9D833A6F0ED"
)

async def main(ble_address):
    # 通过地址找魔方
    device = await BleakScanner.find_device_by_address(ble_address, timeout=30.0)
    if not device:
        print('找不到地址是 {} 的蓝牙设备'.format(ble_address))
        exit()
    # 找到魔方后, 我们便可以操作了它了
    async with BleakClient(device) as client:
        print('已连接到小米智能魔方')
        # 看看魔方提供哪些服务
        cube_services = await client.get_services()
        for service in cube_services:
            print(service)
            for char in service.characteristics:
                print('{} {}'.format(char, char.properties))
            print('--------------------------------')
            
asyncio.run(main(ble_address))

