# -*- coding: utf-8 -*-
'''
Задание 21.5

Создать шаблоны templates/gre_ipsec_vpn_1.txt и templates/gre_ipsec_vpn_2.txt,
которые генерируют конфигурацию IPsec over GRE между двумя маршрутизаторами.

Шаблон templates/gre_ipsec_vpn_1.txt создает конфигурацию для одной стороны туннеля,
а templates/gre_ipsec_vpn_2.txt - для второй.

Примеры итоговой конфигурации, которая должна создаваться на основе шаблонов в файлах:
cisco_vpn_1.txt и cisco_vpn_2.txt.


Создать функцию create_vpn_config, которая использует эти шаблоны для генерации конфигурации VPN на основе данных в словаре data.

Параметры функции:
* template1 - имя файла с шаблоном, который создает конфигурацию для одной строны туннеля
* template2 - имя файла с шаблоном, который создает конфигурацию для второй строны туннеля
* data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна возвращать кортеж с двумя конфигурациямя (строки), которые получены на основе шаблонов.

Примеры конфигураций VPN, которые должна возвращать функция create_vpn_config в файлах
cisco_vpn_1.txt и cisco_vpn_2.txt.
'''

data = {
    'tun_num': 10,
    'wan_ip_1': '192.168.100.1',
    'wan_ip_2': '192.168.100.2',
    'tun_ip_1': '10.0.1.1 255.255.255.252',
    'tun_ip_2': '10.0.1.2 255.255.255.252'
}
from jinja2 import Environment, FileSystemLoader


def create_vpn_config(template1, template2, data_dict):
	template1_dir, template1_file = template1.split('/')
	template2_dir, template2_file = template2.split('/')
	env1 = Environment(
		loader = FileSystemLoader(template1_dir),
		trim_blocks = True,
		lstrip_blocks = True)
	env2 = Environment(
		loader = FileSystemLoader(template2_dir),
		trim_blocks = True,
		lstrip_blocks = True)
	tmpl1 = env1.get_template(template1_file)
	tmpl2 = env2.get_template(template2_file)
	return((tmpl1.render(data_dict), tmpl2.render(data_dict)))
	
	
if __name__ == '__main__':
	template1 = 'templates/gre_ipsec_vpn_1.txt'
	template2 = 'templates/gre_ipsec_vpn_2.txt'
	print(create_vpn_config(template1, template2, data))

