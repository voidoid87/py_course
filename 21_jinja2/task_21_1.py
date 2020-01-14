# -*- coding: utf-8 -*-
'''
Задание 21.1

Создать функцию generate_config.

Параметры функции:
* template - путь к файлу с шаблоном (например, "templates/for.txt")
* data_dict - словарь со значениями, которые надо подставить в шаблон

Функция должна возвращать строку с конфигурацией, которая была сгенерирована.

Проверить работу функции на шаблоне templates/for.txt и данных из файла data_files/for.yml.

'''
from jinja2 import Environment, FileSystemLoader
import yaml

def generate_config(template, data_dict):
	template_dir, template_file = template.split('/')
	env = Environment(
		loader = FileSystemLoader(template_dir),
		trim_blocks = True,
		lstrip_blocks = True)
	tmpl = env.get_template(template_file)
	return(tmpl.render(data_dict))

if __name__=='__main__':
	template = 'templates/for.txt'
	data = 'data_files/for.yml'
	with open(data, 'r') as f:
		data_dict = yaml.safe_load(f)
	print(generate_config(template, data_dict))
