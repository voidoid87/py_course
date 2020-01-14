# -*- coding: utf-8 -*-
'''
Задание 22.1a

Создать функцию parse_output_to_dict.

Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список словарей:
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на выводе команды output/sh_ip_int_br.txt и шаблоне templates/sh_ip_int_br.template.
'''
import textfsm

def parse_output_to_dict(template, command_output):
	r = []
	d = {}
	with open(template) as f:
		re_table = textfsm.TextFSM(f)
		header = re_table.header
		out = re_table.ParseText(command_output)
		r = [{key:val for key, val in zip(header, l)} for l in out]
		return r

		
if __name__ == '__main__':
	with open('output/sh_ip_int_br.txt', 'r') as f:
		command_output = f.read()
	template = 'templates/sh_ip_int_br.template'
	print(parse_output_to_dict(template, command_output))
