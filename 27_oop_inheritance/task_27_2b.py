# -*- coding: utf-8 -*-

'''
Задание 27.2b

Дополнить класс MyNetmiko из задания 27.2a.

Переписать метод send_config_set netmiko, добавив в него проверку на ошибки с помощью метода _check_error_in_command.

Метод send_config_set должен отправлять команды по одной и проверять каждую на ошибки.
Если при выполнении команд не обнаружены ошибки, метод send_config_set возвращает вывод команд.

In [2]: from task_27_2b import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_config_set('lo')
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-2-8e491f78b235> in <module>()
----> 1 r1.send_config_set('lo')

...
ErrorInCommand: При выполнении команды "lo" на устройстве 192.168.100.1 возникла ошибка "Incomplete command."

'''
from netmiko.cisco.cisco_ios import CiscoIosBase

class ErrorInCommand(Exception):
    """При выполнении команды возникла ошибка"""
    pass

device_params = {
    'device_type': 'cisco_ios',
    'ip': '192.168.100.1',
    'username': 'cisco',
    'password': 'cisco',
    'secret': 'cisco'
}

class MyNetmiko(CiscoIosBase):
	def __init__(self, **device_params):
		super().__init__(**device_params)
		self.enable()
	
	def _check_error_in_command(self, command, output):
		if '%' in output:
			for line in output.split('\n'):
				if line.startswith('%'):
					err = line
					break
			msg = 'При выполнении команды "{}" на устройстве {} возникла ошибка {}'.format(command, self.ip, err)
			raise ErrorInCommand(msg)
			return False
		return True
	
	def send_command(self, command):
		output = super().send_command(command)
		self._check_error_in_command(command, output)
		return output	
		
	def send_config_set(self, commands):
		output = ''
		if type(commands) == str:
			commands = [commands]	
		for command in commands:
			output += super().send_config_set(command)
			if self._check_error_in_command(command, output):
				break
			else:
				return output
		
if __name__=='__main__':
	r1 = MyNetmiko(**device_params)
	print(r1.send_config_set('lo'))
	#print(r1.send_command('sh ip br'))
