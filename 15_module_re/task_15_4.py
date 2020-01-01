# -*- coding: utf-8 -*-
'''
Задание 15.4

Создать функцию get_ints_without_description, которая ожидает как аргумент
имя файла, в котором находится конфигурация устройства.


Функция должна обрабатывать конфигурацию и возвращать список имен интерфейсов,
на которых нет описания (команды description).

Пример интерфейса с описанием:
interface Ethernet0/2
 description To P_r9 Ethernet0/2
 ip address 10.0.19.1 255.255.255.0
 mpls traffic-eng tunnels
 ip rsvp bandwidth

Интерфейс без описания:
interface Loopback0
 ip address 10.1.1.1 255.255.255.255

Проверить работу функции на примере файла config_r1.txt.
'''
import re
def get_ints_without_description(configuration):
	result = []
	regintf = r'interface (?P<intf>\w+\d(/\d)?(\.\d+)?)'
	with open(configuration, 'r') as f:
		lines = f.readlines()
	for i in range(len(lines)):
		match = re.search(regintf, lines[i])
		if type(match) == re.Match:
			intf = match.group('intf')
			reg = ' description'
			match = re.search(reg, lines[i+1])
			if type(match) != re.Match:
				result.append(intf)
	return result

if __name__ == '__main__':
	print(get_ints_without_description('config_r1.txt'))
