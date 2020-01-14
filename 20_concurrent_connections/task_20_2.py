# -*- coding: utf-8 -*-
'''
Задание 20.2

Создать функцию send_show_command_to_devices, которая отправляет
одну и ту же команду show на разные устройства в параллельных потоках,
а затем записывает вывод команд в файл.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* command - команда
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.2   YES NVRAM  up                    up
Ethernet0/1                10.1.1.1        YES NVRAM  administratively down down
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down

Для выполнения задания можно создавать любые дополнительные функции.

Проверить работу функции на устройствах из файла devices.yaml
'''
from concurrent.futures import ThreadPoolExecutor
import yaml
import logging
from netmiko import ConnectHandler
from datetime import datetime
from itertools import repeat

logging.basicConfig(format='%(threadName)s %(name)s: %(message)s', level = logging.INFO)

def send_command(device, show):
	result = ''
	logging.info('--> Connecting to {}'.format(device['ip']))
	with ConnectHandler(**device) as s:
		s.enable()
		result = s.find_prompt().strip()
		result = result + s.send_command(show, strip_command = False) + '\n'
		logging.info('<-- Received from {}'.format(device['ip']))
	return result
	
def send_show_command_to_devices(devices, command, filename, limit = 3):
	with ThreadPoolExecutor(max_workers = limit) as executor:
		r = list(executor.map(send_command, devices, repeat(command)))
	with open(filename, 'w') as f:
		f.writelines(r)

if __name__ == '__main__':
	command = 'sh ip int br'
	with open('devices.yaml', 'r') as yml:
		devices = yaml.safe_load(yml)
	send_show_command_to_devices(devices, command, 'output.txt')
	
	
	
	
	
	
	
	
	
	
