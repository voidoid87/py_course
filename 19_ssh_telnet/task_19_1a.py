# -*- coding: utf-8 -*-
'''
Задание 19.1a

Скопировать функцию send_show_command из задания 19.1 и переделать ее таким образом,
чтобы обрабатывалось исключение, которое генерируется
при ошибке аутентификации на устройстве.

При возникновении ошибки, на стандартный поток вывода должно выводиться сообщение исключения.

Для проверки измените пароль на устройстве или в файле devices.yaml.
'''
command = 'sh ip int br'

import netmiko
import yaml

def send_show_command(device, command):
	try:
		with netmiko.ConnectHandler(**device) as s:
			s.enable()
			return(s.send_command(command))
	except netmiko.ssh_exception.NetMikoAuthenticationException as e:
		print(str(e))

if __name__ == '__main__':
	with open('devices.yaml', 'r') as f:
		d = yaml.safe_load(f)
	for device in d:
		print(send_show_command(device, command))
