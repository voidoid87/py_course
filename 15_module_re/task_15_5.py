# -*- coding: utf-8 -*-
'''
Задание 15.5

Создать функцию generate_description_from_cdp, которая ожидает как аргумент
имя файла, в котором находится вывод команды show cdp neighbors.

Функция должна обрабатывать вывод команды show cdp neighbors и генерировать на основании вывода команды описание для интерфейсов.

Например, если у R1 такой вывод команды:
R1>show cdp neighbors
Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
                  S - Switch, H - Host, I - IGMP, r - Repeater

Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
SW1              Eth 0/0           140          S I      WS-C3750-  Eth 0/1

Для интерфейса Eth 0/0 надо сгенерировать такое описание
description Connected to SW1 port Eth 0/1

Функция должна возвращать словарь, в котором ключи - имена интерфейсов, а значения - команда задающая описание интерфейса:
'Eth 0/0': 'description Connected to SW1 port Eth 0/1'


Проверить работу функции на файле sh_cdp_n_sw1.txt.
'''
import re
def generate_description_from_cdp(output):
	result = {}
	reg = re.compile(r'(?P<dest>\w\w?\d)\s+(?P<intf>\w{3}\s\d\/\d).+(?P<port>\w{3}\s\d\/\d)$')  
	with open(output, 'r') as f:
		for line in f:
			match = re.search(reg, line)
			if type(match) == re.Match:
				result[match.group('intf')] = f"description Connected to {match.group('dest')} port {match.group('port')}"
	return result
			

		
	
if __name__ == '__main__':
	print(generate_description_from_cdp('sh_cdp_n_sw1.txt'))
