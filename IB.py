import asyncio
from bleak import BleakScanner
import time
import matplotlib.pyplot as plt

cl_dic = {}
room = {}
mac_add = "65:78:66:04:9E:6F"
# tar_mac = "C4:89:55:42:E3:85"
tar_mac = "65:78:66:04:9E:6F"
non_leave = True

# Case study on setting the closest IBeacon = mac_addm, the target IBeacon = tar_mac.

class device:
    gen_info = "Please wear mask properly and keep the social distancing"

    def __init__(self, name, addr, add_info='', info=gen_info):
        self.name = name
        self.addr = addr
        self.info = info + add_info
        room[addr] = [name, self.info]


room101 = device("room101", mac_add, "\nSit Alternately is required in study room.")
room103 = device("room103", tar_mac, "\nExhibition Talks tonight at room103")

def check_leave(device, advertisement_data):
    print(device.address, "RSSI:", device.rssi, advertisement_data)
    if device.address == tar_mac and int(device.rssi)*-1 > 60:
        non_leave = False
        return False
    else:
        return True


def detection_callback(device, advertisement_data):
    print(device.address, "RSSI:", device.rssi, advertisement_data)
    if int(device.rssi) * -1 < 50:
        cl_dic[str(device.address)] = device.rssi


async def main():
    scanner = BleakScanner()
    scanner.register_detection_callback(detection_callback)
    await scanner.start()
    await asyncio.sleep(5.0)
    await scanner.stop()


asyncio.run(main())

async def check_le():
    scanner2 = BleakScanner()
    st_fl = scanner2.register_detection_callback(check_leave)
    if st_fl == False:
        return False
    await scanner2.start()
    await asyncio.sleep(1.0)
    await scanner2.stop()
    return True

def getinfo(mac):
    try:
        print("You are entering " + str(room[mac][0]) + ',' + str(room[mac][1]))
    except:
        print("Please setup the mac information first")


def nav(mac):
    print("Please move forward to room103")

stop_flag = True
if cl_dic:
    sm_mac = min(cl_dic, key=cl_dic.get)
    print("\n")
    getinfo(sm_mac)
    if sm_mac != tar_mac:
        nav(tar_mac)
    else:
        start_time = time.time()
        while (non_leave):
            stop_flag = asyncio.run(check_le())
            if stop_flag == False:
                break
        end_time = time.time()
        print(f"You are leaving {room[tar_mac][0]}")
        print(f"Study time: {end_time - start_time}  seconds")

else:
    print("not found any devices nearby, please keep walking")
