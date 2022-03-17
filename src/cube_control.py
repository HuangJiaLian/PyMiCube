import asyncio, signal, pyautogui
from bleak import BleakScanner, BleakClient

ble_address = '9A8BE917-31DE-C67E-48C4-E9D833A6F0ED'
uuid = '0000aadc-0000-1000-8000-00805f9b34fb'

# value is to store the data received
# pre_value is to store the last data received 
pre_value, value = -1, -1

# when new data comes
def notification_handler(sender, data):
    global value
    value = data 

END = False
# when Ctrl + C pressed
def sigint_handler(signum, frame):
    global END
    END = True
    print('Interrupted!')
# register the interrupt handler
signal.signal(signal.SIGINT, sigint_handler)

key = [176, 81, 104, 224, 86, 137,
       237, 119, 38, 26,  193, 161,
       210, 126, 150, 81, 93, 13,
       236, 249, 89, 235, 88, 24, 
       113, 81, 214, 131, 130, 199,
       2,  169, 39, 165, 171, 41]

def toHexVal(value, key):
    raw = list(value)
    k1 = raw[-1] >> 4 & 0xf
    k2 = raw[-1] & 0xf 
    # decode the value
    for i in range(18):
        raw[i] += key[i+k1] + key[i+k2]
    raw = raw[:18]
    
    # save each half byte in a list
    valhex = []
    for i in range(len(raw)):
        valhex.append(raw[i] >> 4 & 0xf)
        valhex.append(raw[i] & 0xf)
    return valhex


async def main(ble_address, uuid):
    global pre_value, value 
    device = await BleakScanner.find_device_by_address(ble_address, timeout=30)
    async with BleakClient(device) as client:
        print('Mi Smart Magic Cube connected.')
        await client.start_notify(uuid, notification_handler)
        while True:
            if value != pre_value:
                pre_value = value
                valhex = toHexVal(value, key)
                print(valhex)
                # valhex[-3]: 1 for clockwise rotation, 3 for anticlockwise
                anticlockwise = True if valhex[-3] ==3 else False
                
                # MagicCube 
                # valhex[-4]:  1,2,3,4,5,6 for B, Y, O, W, R, G
                #press_key = 'RDBUFL'[valhex[-4]-1]
                #if anticlockwise:
                #    pyautogui.hotkey(' ', press_key)
                #else:
                #    pyautogui.typewrite(press_key)

                # Musicbox
                if valhex[-4] == 1:
                    pyautogui.typewrite(' ')
                if valhex[-4] == 6:
                    if anticlockwise:
                        pyautogui.typewrite('[')
                    else:
                        pyautogui.typewrite(']')
            else:
                await asyncio.sleep(0.1)
            if END == True:
                break
        await client.stop_notify(uuid)

asyncio.run(main(ble_address, uuid))
