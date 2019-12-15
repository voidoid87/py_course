#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет доступность IP-адресов.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте ping.

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''
import ipaddress, subprocess

def ping_ip_addresses(iplist):
	out = tuple()
	out = [],[]
	
	for ip in iplist:
		reply = subprocess.run(['ping', '-c', '3', '-n', ip], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL, encoding = 'utf-8')
		if reply.returncode == 0:
			out[0].append(ip)
		else:
			out[1].append(ip)
	return out

if __name__ == '__main__':
	list_of_ips = ['1.1.1', '8.8.8.8', '8.8.4.4', '8.8.7.1']
	print(ping_ip_addresses(list_of_ips))
	
		

