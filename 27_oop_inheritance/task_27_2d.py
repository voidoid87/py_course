# -*- coding: utf-8 -*-

'''
Задание 27.2d

Дополнить класс MyNetmiko из задания 27.2c или задания 27.2b.

Добавить параметр ignore_errors в метод send_config_set.
Если передано истинное значение, не надо выполнять проверку на ошибки и метод должен работать точно так же как метод send_config_set в netmiko.

Если значение ложное, ошибки должны проверяться.

По умолчанию ошибки должны игнорироваться.


In [2]: from task_27_2d import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [6]: r1.send_config_set('lo')
Out[6]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [7]: r1.send_config_set('lo', ignore_errors=True)
Out[7]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [8]: r1.send_config_set('lo', ignore_errors=False)
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-8-704f2e8d1886> in <module>()
----> 1 r1.send_config_set('lo', ignore_errors=False)

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
	
	def send_command(self, command, **kwargs):
		output = super().send_command(command, **kwargs)
		self._check_error_in_command(command, output)
		return output	
		
	def send_config_set(self, commands, ignore_errors=True):
		if  ignore_errors:
			return super().send_config_set(commands)
		else:
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
	print(r1.send_command('sh ip int br', strip_command=True))
