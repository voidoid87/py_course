# -*- coding: utf-8 -*-

'''
Задание 25.2c

Скопировать класс CiscoTelnet из задания 25.2b и изменить метод send_config_commands добавив проверку команд на ошибки.

У метода send_config_commands должен быть дополнительный параметр strict:
* strict=True значит, что при обнаружении ошибки, необходимо сгенерировать исключение ValueError
* strict=False значит, что при обнаружении ошибки, надо только вывести на стандартный поток вывода сообщене об ошибке

Метод дожен возвращать вывод аналогичный методу send_config_set у netmiko (пример вывода ниже).
Текст исключения и ошибки в примере ниже.

Пример создания экземпляра класса:
In [1]: from task_25_2c import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

In [4]: commands_with_errors = ['logging 0255.255.1', 'logging', 'i']
In [5]: correct_commands = ['logging buffered 20010', 'ip http server']
In [6]: commands = commands_with_errors+correct_commands

Использование метода send_config_commands:

In [7]: print(r1.send_config_commands(commands, strict=False))
При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.
При выполнении команды "logging" на устройстве 192.168.100.1 возникла ошибка -> Incomplete command.
При выполнении команды "i" на устройстве 192.168.100.1 возникла ошибка -> Ambiguous command:  "i"
conf t
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.

R1(config)#logging
% Incomplete command.

R1(config)#i
% Ambiguous command:  "i"
R1(config)#logging buffered 20010
R1(config)#ip http server
R1(config)#end
R1#

In [8]: print(r1.send_config_commands(commands, strict=True))
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-8-0abc1ed8602e> in <module>
----> 1 print(r1.send_config_commands(commands, strict=True))

...

ValueError: При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.

'''

import telnetlib
import textfsm
import time
import re

class CiscoTelnet:
	def __init__(self, ip, username, password, secret):
		self.ip = ip
		self.telnet = telnetlib.Telnet(ip)
		self.telnet.read_until(b'Username')
		self._write_line(username)
		self.telnet.read_until(b'Password')
		self._write_line(password)
		self._write_line('enable')
		self.telnet.read_until(b'Password')
		self._write_line(secret)
		self.telnet.read_until(b'#')
		self._write_line('terminal length 0')
		self.telnet.read_until(b'#')
		
	def _write_line(self, string):
		self.telnet.write((string+'\n').encode('ascii'))
		
	def send_show_command(self, show, parse, templates='templates'):
		self._write_line(show)	
		result = self.telnet.read_until(b'#').decode('utf-8')
		self.telnet.close()
		if not parse:
			return(result)
		else:
			with open(templates+'/sh_ip_int_br.template') as f:
				re_table = textfsm.TextFSM(f)
				header = re_table.header
				out = re_table.ParseText(result)
				return([{key:val for key, val in zip(header, l)} for l in out])
				

	def send_config_commands(self, commands, strict=False):
		result = ''
		if type(commands)==str:
			commands = [commands]
		self._write_line('configure terminal')
		result = result + self.telnet.read_until(b'#').decode('utf-8')
		for command in commands:
				self._write_line(command)
				reply = self.telnet.read_until(b'#').decode('utf-8')
				result = result + reply
				if '%' in reply:
					err_cli = reply.split('\n')[-3]
					msg = 'При выполнении команды "{}" на устройстве {} возникла ошибка -> {}'.format(command, self.ip, err_cli)
					if strict:
						raise ValueError(msg)
					else:
						print(msg)
		self._write_line('end')
		time.sleep(1)
		return(result)
		
if __name__ == '__main__':
	
	r1_params = {
				'ip': '192.168.100.1',
				'username': 'cisco',
				'password': 'cisco',
				'secret': 'cisco'}	
					
	r1 = CiscoTelnet(**r1_params)	
	commands_with_errors = ['logging 0255.255.1', 'logging', 'i']
	correct_commands = ['logging buffered 20010', 'ip http server']
	commands = commands_with_errors+correct_commands
	print(r1.send_config_commands(commands, strict = False))	
		
