# -*- coding: utf-8 -*-
'''
Задание 12.3


Создать функцию print_ip_table, которая отображает таблицу доступных и недоступных IP-адресов.

Функция ожидает как аргументы два списка:
* список доступных IP-адресов
* список недоступных IP-адресов

Результат работы функции - вывод на стандартный поток вывода таблицы вида:

Reachable    Unreachable
-----------  -------------
10.1.1.1     10.1.1.7
10.1.1.2     10.1.1.8
             10.1.1.9

Функция не должна изменять списки, которые переданы ей как аргументы.
То есть, до выполнения функции и после списки должны выглядеть одинаково.


Для этого задания нет тестов
'''
import sys
sys.path.append('/home/python/venv/pyneng-py3-7/lib/python3.7/site-packages')
from tabulate import tabulate

def print_ip_table(reached, unreached):
	result = []
	r = len(reached)
	u = len(unreached)
	if r > u:
		c = r - u
		k = 1
	elif r < u:
		c = u - r
		k = 0
	result = list(zip(reached, unreached))
	if c:
		for i in range(c,0,-1):
			if not k:
				result.append(('', unreached[-i]))
			elif k:
				result.append((reached[-i],''))
			
	columns = ['Reachable', 'Unreachable']
	print(tabulate(result, headers = columns))

if __name__ == '__main__':
	r = ['10.1.1.1', '10.1.1.2']
	u = ['10.1.1.7', '10.1.1.8','10.1.1.9']
	print_ip_table(r, u)
