# -*- coding: utf-8 -*-
'''
Задание 22.5

Создать функцию send_and_parse_command_parallel.

Функция send_and_parse_command_parallel должна запускать в параллельных потоках функцию send_and_parse_show_command из задания 22.4.

В этом задании надо самостоятельно решить:
* какие параметры будут у функции
* что она будет возвращать


Теста для этого задания нет.
'''
from task_22_4 import send_and_parse_show_command
from concurrent.futures import ThreadPoolExecutor, as_completed
import yaml

def send_and_parse_command_parallel(device_list, command, limit = 3):
	with ThreadPoolExecutor(max_workers = limit) as executor:
		flist = [executor.submit(send_and_parse_show_command, device_dict, command) for device_dict in device_list]
		return([f.result() for f in as_completed(flist)])
	
	
if __name__ == '__main__':
	command = 'sh ip int br'
	with open('devices.yaml', 'r') as f:
		device_list = yaml.safe_load(f)
	print(send_and_parse_command_parallel(device_list, command))
	
