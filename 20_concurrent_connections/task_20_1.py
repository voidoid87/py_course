# -*- coding: utf-8 -*-
'''
Задание 20.1

Создать функцию ping_ip_addresses, которая проверяет доступность IP-адресов.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.
'''

import netmiko
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
import logging
from datetime import datetime




logging.basicConfig(
    format='%(threadName)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO)

def ping_ip(ip):
	msg = '---> {} ping {}'
	logging.info(msg.format(datetime.now().time(), ip))
	reply = subprocess.run(['ping', '-c', '3', '-n', ip], stdout = subprocess.PIPE, encoding = 'utf-8')
	return(reply.returncode)
    
def ping_ip_addresses(ip_list, limit=3):
	reach, unreach = [], []
	with ThreadPoolExecutor(max_workers=limit) as executor:
		result = executor.map(ping_ip, ip_list)
		for ip, rcode in zip(ip_list, result):
			if rcode == 0:
				reach.append(ip)
			else:
				unreach.append(ip)
			
	return((reach, unreach))
	
if __name__ == '__main__':
	ip_list = ['8.8.8.8', '4.4.4.4', '192.168.100.100', '192.168.100.1', '10.0.0.0', '192.168.100.2']
	print(ping_ip_addresses(ip_list))
