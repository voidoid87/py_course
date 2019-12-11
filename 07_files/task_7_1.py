# -*- coding: utf-8 -*-
'''
Задание 7.1

Аналогично заданию 4.6 обработать строки из файла ospf.txt
и вывести информацию по каждой в таком виде:
Protocol:              OSPF
Prefix:                10.0.24.0/24
AD/Metric:             110/41
Next-Hop:              10.0.13.3
Last update:           3d18h
Outbound Interface:    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

with open('ospf.txt', 'r') as file:
	for line in file:
		ospf = line.split()
		print('{:25}{:15}\n{:25}{:15}\n{:25}{:15}\n{:25}{:15}\n{:25}{:15}\n{:25}{:15}\n'.format('Protocol:', 'OSPF', 'Prefix:', ospf[1], 'AD/Metric:', ospf[2].strip('[]'), 'Next-Hop:', ospf[4].strip(','), 'Last update:', ospf[5].strip(','), 'Outbound Interface:', ospf[6]))
