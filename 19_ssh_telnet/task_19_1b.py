# -*- coding: utf-8 -*-
'''
Задание 19.1b

Скопировать функцию send_show_command из задания 19.1a и переделать ее таким образом,
чтобы обрабатывалось не только исключение, которое генерируется
при ошибке аутентификации на устройстве, но и исключение,
которое генерируется, когда IP-адрес устройства недоступен.

При возникновении ошибки, на стандартный поток вывода должно выводиться сообщение исключения.

Для проверки измените IP-адрес на устройстве или в файле devices.yaml.
'''
command = 'sh ip int br'

import netmiko
import yaml

def send_show_command(device, command):
	try:
		with netmiko.ConnectHandler(**device) as s:
			s.enable()
			return(s.send_command(command))
	except (netmiko.ssh_exception.NetMikoAuthenticationException, 
			netmiko.ssh_exception.NetMikoTimeoutException) as e:
		print(str(e))

if __name__ == '__main__':
	with open('devices.yaml', 'r') as f:
		d = yaml.safe_load(f)
	for device in d:
		print(send_show_command(device, command))
