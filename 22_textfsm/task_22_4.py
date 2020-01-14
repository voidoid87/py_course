# -*- coding: utf-8 -*-
'''
Задание 22.4

Создать функцию send_and_parse_show_command.

Параметры функции:
* device_dict - словарь с параметрами подключения к одному устройству
* command - команда, которую надо выполнить
* templates_path - путь к каталогу с шаблонами TextFSM
* index - имя индекс файла, значение по умолчанию "index"

Функция должна подключаться к одному устройству, отправлять команду show с помощью netmiko,
а затем парсить вывод команды с помощью TextFSM.

Функция должна возвращать список словарей с результатами обработки вывода команды (как в задании 22.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br и устройствах из devices.yaml.
'''
from netmiko import ConnectHandler
import clitable
import yaml

def send_and_parse_show_command(device_dict, command, templates_path = 'templates', index = 'index'):
	cli = clitable.CliTable(index, templates_path)
	attrib = {'Command': command, 'Vendor': device_dict['device_type']}
	with ConnectHandler(**device_dict) as ssh:
		ssh.enable()
		out = ssh.send_command(command)
	cli.ParseCmd(out, attrib)
	header = list(cli.header)
	out = [list(row) for row in cli]
	r = [{key:val for key, val in zip(header, l)} for l in out]
	return r
		
if __name__ == '__main__':
	command = 'sh ip int br'
	with open('devices.yaml', 'r') as f:
		device_list = yaml.safe_load(f)
	for device_dict in device_list:
		print(send_and_parse_show_command(device_dict, command))
	
