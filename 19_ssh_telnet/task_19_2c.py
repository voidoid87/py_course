# -*- coding: utf-8 -*-
'''
Задание 19.2c

Скопировать функцию send_config_commands из задания 19.2b и переделать ее таким образом:

Если при выполнении команды возникла ошибка,
спросить пользователя надо ли выполнять остальные команды.

Варианты ответа [y]/n:
* y - выполнять остальные команды. Это значение по умолчанию, поэтому нажатие любой комбинации воспринимается как y
* n или no - не выполнять остальные команды

Функция send_config_commands по-прежнему должна возвращать кортеж из двух словарей:
* первый словарь с выводом команд, которые выполнились без ошибки
* второй словарь с выводом команд, которые выполнились с ошибками

Оба словаря в формате
* ключ - команда
* значение - вывод с выполнением команд

Проверить работу функции можно на одном устройстве.

Пример работы функции:

In [11]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...
Команда "logging 0255.255.1" выполнилась с ошибкой "Invalid input detected at '^' marker." на устройстве 192.168.100.1
Продолжать выполнять команды? [y]/n: y
Команда "logging" выполнилась с ошибкой "Incomplete command." на устройстве 192.168.100.1
Продолжать выполнять команды? [y]/n: n

In [12]: pprint(result)
({},
 {'logging': 'config term\n'
             'Enter configuration commands, one per line.  End with CNTL/Z.\n'
             'R1(config)#logging\n'
             '% Incomplete command.\n'
             '\n'
             'R1(config)#',
  'logging 0255.255.1': 'config term\n'
                        'Enter configuration commands, one per line.  End with '
                        'CNTL/Z.\n'
                        'R1(config)#logging 0255.255.1\n'
                        '                   ^\n'
                        "% Invalid input detected at '^' marker.\n"
                        '\n'
                        'R1(config)#'})

'''
import netmiko
import yaml

def send_config_commands(device, config_commands, verbose = True):
	clear = {}
	error = {}
	if verbose:
		print('Connecting to ' + device['ip'])
	try:
		with netmiko.ConnectHandler(**device) as s:
			s.enable()
			for command in config_commands:
				reply = s.send_config_set(command)
				if '%' in reply:
					print('Command '+ command + ' completed with an error ' + reply.split('%')[-1].split('\n')[0] + ' on device ' + device['ip'])
					error[command] = reply
					c = input('Continue to execute next commands? [y]/n:')
					if 'n' in c:
						break
				else:
					clear[command] = reply
	except (netmiko.ssh_exception.NetMikoAuthenticationException, 
			netmiko.ssh_exception.NetMikoTimeoutException) as e:
		print(str(e))
	return((clear, error))

# списки команд с ошибками и без:
commands_with_errors = ['logging 0255.255.1', 'logging', 'a']
correct_commands = ['logging buffered 20010', 'ip http server']

commands = commands_with_errors + correct_commands

if __name__ == '__main__':
	with open('devices.yaml', 'r') as f:
		d = yaml.safe_load(f)
	for device in d:
		print(send_config_commands(device, commands))

