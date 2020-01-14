# -*- coding: utf-8 -*-
'''
Задание 22.1

Создать функцию parse_command_output. Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список:
* первый элемент - это список с названиями столбцов
* остальные элементы это списки, в котором находятся результаты обработки вывода

Проверить работу функции на выводе команды output/sh_ip_int_br.txt и шаблоне templates/sh_ip_int_br.template.

'''
import textfsm

def parse_command_output(template, command_output):
	r = []
	with open(template) as f:
		re_table = textfsm.TextFSM(f)
		header = re_table.header
		out = re_table.ParseText(command_output)
		out.insert(0, header)
		return out

		
if __name__ == '__main__':
	with open('output/sh_ip_int_br.txt', 'r') as f:
		command_output = f.read()
	template = 'templates/sh_ip_int_br.template'
	print(parse_command_output(template, command_output))
