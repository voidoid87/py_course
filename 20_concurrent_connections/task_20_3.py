# -*- coding: utf-8 -*-
'''
Задание 20.3

Создать функцию send_command_to_devices, которая отправляет
разные команды show на разные устройства в параллельных потоках,
а затем записывает вывод команд в файл.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* commands_dict - словарь в котором указано на какое устройство отправлять какую команду. Пример словаря - commands
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.100.1          76   aabb.cc00.6500  ARPA   Ethernet0/0
Internet  192.168.100.2           -   aabb.cc00.6600  ARPA   Ethernet0/0
Internet  192.168.100.3         173   aabb.cc00.6700  ARPA   Ethernet0/0
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down


Для выполнения задания можно создавать любые дополнительные функции.

Проверить работу функции на устройствах из файла devices.yaml и словаре commands
'''
from concurrent.futures import ThreadPoolExecutor, as_completed
import yaml
import logging
from netmiko import ConnectHandler
from datetime import datetime
from itertools import repeat

commands = {'192.168.100.1': 'sh ip int br',
            '192.168.100.2': 'sh arp',
            '192.168.100.3': 'sh ip int br'}


logging.basicConfig(format='%(threadName)s %(name)s: %(message)s', level = logging.INFO)

def send_command(device, command):
	result = ''
	logging.info('--> Connecting to {}'.format(device['ip']))
	with ConnectHandler(**device) as s:
		s.enable()
		result = s.find_prompt().strip()
		result = result + s.send_command(command, strip_command = False) + '\n'
		logging.info('<-- Received from {}'.format(device['ip']))
	return result
	
def send_command_to_devices(devices, command_dict, filename, limit = 3):
	with ThreadPoolExecutor(max_workers = limit) as executor:
		future_list = [executor.submit(send_command, device, command_dict[device['ip']]) for device in devices]
	with open(filename, 'w') as f:
		for block in as_completed(future_list):
			f.write(block.result())

if __name__ == '__main__':

	with open('devices.yaml', 'r') as yml:
		devices = yaml.safe_load(yml)
	send_command_to_devices(devices, commands, 'output_20_3.txt')
	
	
	
	
	
