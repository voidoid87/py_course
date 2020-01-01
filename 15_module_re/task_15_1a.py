# -*- coding: utf-8 -*-
'''
Задание 15.1a

Скопировать функцию get_ip_from_cfg из задания 15.1 и переделать ее таким образом, чтобы она возвращала словарь:
* ключ: имя интерфейса
* значение: кортеж с двумя строками:
  * IP-адрес
  * маска

В словарь добавлять только те интерфейсы, на которых настроены IP-адреса.

Например (взяты произвольные адреса):
{'FastEthernet0/1':('10.0.1.1', '255.255.255.0'),
 'FastEthernet0/2':('10.0.2.1', '255.255.255.0')}

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла config_r1.txt.

Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды, а не ввод пользователя.

'''
import re
def get_ip_from_cfg(filename):
	result = {}
	net = tuple()
	regintf = r'interface (?P<intf>\w+\d(/\d)?)'
	regip = 'ip address\s(?P<ip>(\d+\.){3}\d+)\s(?P<mac>(\d+\.){3}\d+)'
	with open(filename, 'r') as f:
		for line in f:
			match = re.search(regintf, line)
			if type(match) == re.Match:
				intf = match.group('intf')
				continue
			match = re.search(regip, line)
			if type(match) == re.Match: 
				result[intf] = match.group('ip'), match.group('mac')
	return result
	
print(get_ip_from_cfg('config_r1.txt'))
