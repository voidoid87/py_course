#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Задание 7.2c

Переделать скрипт из задания 7.2b:
* передавать как аргументы скрипту:
 * имя исходного файла конфигурации
 * имя итогового файла конфигурации

Внутри, скрипт должен отфильтровать те строки, в исходном файле конфигурации,
в которых содержатся слова из списка ignore.
И записать остальные строки в итоговый файл.

Проверить работу скрипта на примере файла config_sw1.txt.

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

ignore = ['duplex', 'alias', 'Current configuration']

from sys import argv
with open(argv[1], 'r') as f, open(argv[2] ,'w') as fc:
	for line in f:
		for exc in ignore:
			if line.find(exc) == -1:
				continue
			else:
				break
		else:
			fc.write(line + '\n')
					

