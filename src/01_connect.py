import asyncio
from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError

# 物理地址
ble_address = "D8:99:3A:4A:9E:8D"
receive_UUID = "0000aadc-0000-1000-8000-00805f9b34fb"

key = [176,  81, 104, 224,  86, 137,
       237, 119,  38,  26, 193, 161,
       210, 126, 150,  81,  93,  13, 
       236, 249,  89, 235,  88,  24, 
       113,  81, 214, 131, 130, 199, 
         2, 169,  39, 165, 171, 41]

def print_hex(bytes):
    l = [hex(int(i)) for i in bytes]
    return(" ".join(l))

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

async def main(ble_address):
    device = await BleakScanner.find_device_by_address(ble_address, timeout=20.0)
    if not device:
        raise BleakError(f"A device with address {ble_address} could not be found.")
    
    async with BleakClient(device) as client:
        print('XiaoMi Magic Cube connected.')
        while True:
            value = await client.read_gatt_char(receive_UUID)
            valhex = toHexVal(value, key)
            # print(model_number)
            # print(type(model_number))
            # print(model_number[0], model_number[-2])
            # print(print_hex(model_number))
            print(valhex)
            


asyncio.run(main(ble_address))




# Ref.
# [1] https://juejin.cn/post/7024431647638421540
# [2] https://www.youtube.com/watch?v=1pIV4bjYAK4&t=454s
# [3] https://medium.com/@juananclaramunt/xiaomi-mi-smart-rubik-cube-ff5a22549f90
# [4] https://github.com/cs0x7f/cstimer/blob/master/src/js/bluetooth.js
