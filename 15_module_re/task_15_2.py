# -*- coding: utf-8 -*-
'''
Задание 15.2

Создать функцию parse_sh_ip_int_br, которая ожидает как аргумент
имя файла, в котором находится вывод команды show ip int br

Функция должна обрабатывать вывод команды show ip int br и возвращать такие поля:
* Interface
* IP-Address
* Status
* Protocol

Информация должна возвращаться в виде списка кортежей:
[('FastEthernet0/0', '10.0.1.1', 'up', 'up'),
 ('FastEthernet0/1', '10.0.2.1', 'up', 'up'),
 ('FastEthernet0/2', 'unassigned', 'down', 'down')]

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла sh_ip_int_br.txt.

'''
import re
def parse_sh_ip_int_br(filename):
	regex = re.compile(r'(?P<intf>\S+\d+(/\d)?) +(?P<ip>(\d+\.){3}\d+|unassigned) +\w+ +\w+ +(?P<status>up|down|administratively down) +(?P<proto>up|down)')
	with open(filename, 'r') as f:
		result = [match.group('intf', 'ip', 'status', 'proto') for match in re.finditer(regex, f.read())]
	return result

if __name__ == '__main__':	
	print(parse_sh_ip_int_br('sh_ip_int_br.txt'))
			
	
