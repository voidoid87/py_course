# -*- coding: utf-8 -*-
'''
Задание 19.1

Создать функцию send_show_command.

Функция подключается по SSH (с помощью netmiko) к одному устройству и выполняет указанную команду.

Параметры функции:
* device - словарь с параметрами подключения к устройству
* command - команда, которую надо выполнить

Функция возвращает строку с выводом команды.

Скрипт должен отправлять команду command на все устройства из файла devices.yaml с помощью функции send_show_command.

'''

command = 'sh ip int br'

from netmiko import ConnectHandler
import yaml

def send_show_command(device, command):
	with ConnectHandler(**device) as s:
		s.enable()
		return(s.send_command(command))

if __name__ == '__main__':
	with open('devices.yaml', 'r') as f:
		d = yaml.safe_load(f)
	for device in d:
		print(send_show_command(device, command))
