# -*- coding: utf-8 -*-
'''
Задание 17.2

Создать функцию parse_sh_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой (не имя файла).
Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.


Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt
'''

def parse_sh_cdp_neighbors(output):
	s = {}
	output = output.strip()
	host = output[:output.find('>')] 
	s[host] = {}
	out = output.split('\n')
	for i in range(len(out)):
		if 'Device ID' in out[i]:
			for k in range(i+1, len(out)):
				ln = out[k].split()
				s[host][ln[1] + ' ' + ln[2]] = {}
				s[host][ln[1] + ' ' + ln[2]][ln[0]] = ln[-2] + ' ' + ln[-1]
			break
	return s
				
				

if __name__ == '__main__':
	with open('sh_cdp_n_sw1.txt', 'r') as f:
		output = f.read()
	print(parse_sh_cdp_neighbors(output))
