# -*- coding: utf-8 -*-
'''
Задание 21.5a

Создать функцию configure_vpn, которая использует шаблоны из задания 21.5 для настройки VPN на маршрутизаторах на основе данных в словаре data.

Параметры функции:
* src_device_params - словарь с параметрами подключения к устройству
* dst_device_params - словарь с параметрами подключения к устройству
* src_template - имя файла с шаблоном, который создает конфигурацию для одной строны туннеля
* dst_template - имя файла с шаблоном, который создает конфигурацию для второй строны туннеля
* vpn_data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна настроить VPN на основе шаблонов и данных на каждом устройстве.
Функция возвращает вывод с набором команд с двух марушртизаторов (вывод, которые возвращает send_config_set).

При этом, в словаре data не указан номер интерфейса Tunnel, который надо использовать.
Номер надо определить самостоятельно на основе информации с оборудования.
Если на маршрутизаторе нет интерфейсов Tunnel, взять номер 0, если есть взять ближайший свободный номер,
но одинаковый для двух маршрутизаторов.

Например, если на маршрутизаторе src такие интерфейсы: Tunnel1, Tunnel4.
А на маршрутизаторе dest такие: Tunnel2, Tunnel3, Tunnel8.
Первый свободный номер одинаковый для двух маршрутизаторов будет 9.
И надо будет настроить интерфейс Tunnel 9.

Для этого задания нет теста!
'''
from netmiko import ConnectHandler
from concurrent.futures import ThreadPoolExecutor, as_completed
import yaml
import logging
from task_21_5 import create_vpn_config

data = {
    'tun_num': None,
    'wan_ip_1': '192.168.100.1',
    'wan_ip_2': '192.168.100.2',
    'tun_ip_1': '10.0.1.1 255.255.255.252',
    'tun_ip_2': '10.0.1.2 255.255.255.252'
}
def connect_to_device(params):
	logging.info('--> Connecting to {}'.format(params['ip']))
	ssh = ConnectHandler(**params)
	return ssh

def send_conf(ssh, conf):
	return(ssh.send_config_set(conf))
	
def send_command(ssh, command):
	ssh.enable()
	return(ssh.send_command(command))

	
def get_interface_list(ssh):
	out = send_command(ssh, 'sh tun tun').split('\n')[1:]
	if out:
		return([line.split()[0] for line in out])
	else:
		return []


def define_tunnel_number(list1, list2):
	num = 0
	while True:
		i = str(num)
		if not (i in list1) and not (i in list2):
			return(num)
		num+=1

def multithread_run(func, *args):
	c = len(args)
	if c<3:
		workers = 3
	elif c>12:
		workers = 12
	else:
		workers = c
	
	with ThreadPoolExecutor(max_workers = workers) as executor:
		if c == 1:
			 flist = [executor.submit(func, arg) for arg in args[0]]
		elif c > 1:
			flist = [executor.submit(func, *tup) for tup in zip(*args)]
	return([f.result() for f in as_completed(flist)])
 
	
def configure_vpn(src_device_params, dst_device_params, src_template, dst_template, vpn_data_dict):
	params = [src_device_params, dst_device_params]
	r = multithread_run(connect_to_device, params)
	intf_list = multithread_run(get_interface_list, r)
	vpn_data_dict['tun_num'] = define_tunnel_number(*intf_list)
	conf_tup = create_vpn_config(src_template, dst_template, vpn_data_dict)
	return(multithread_run(send_conf, r, conf_tup))

		
if __name__ == '__main__':
	logging.basicConfig(
		format='%(threadName)s %(name)s %(levelname)s: %(message)s',
		level=logging.INFO)
	with open('devices.yaml' , 'r') as f:
		dicts = yaml.safe_load(f)
	src_device_params, dst_device_params = dicts
	src_template = 'templates/gre_ipsec_vpn_1.txt'
	dst_template = 'templates/gre_ipsec_vpn_2.txt'
	print(configure_vpn(src_device_params, dst_device_params, src_template, dst_template, data))
	
