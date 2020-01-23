# -*- coding: utf-8 -*-

'''
Задание 26.2

Добавить к классу CiscoTelnet из задания 25.2x поддержку работы в менеджере контекста.
При выходе из блока менеджера контекста должно закрываться соединение.
Все исключения, которые возникли в менеджере контекста, должны генерироваться после выхода из блока with.

Пример работы:

In [14]: r1_params = {
    ...:     'ip': '192.168.100.1',
    ...:     'username': 'cisco',
    ...:     'password': 'cisco',
    ...:     'secret': 'cisco'}

In [15]: from task_26_2 import CiscoTelnet

In [16]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:
sh clock
*19:17:20.244 UTC Sat Apr 6 2019
R1#

In [17]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:     raise ValueError('Возникла ошибка')
    ...:
sh clock
*19:17:38.828 UTC Sat Apr 6 2019
R1#
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-17-f3141be7c129> in <module>
      1 with CiscoTelnet(**r1_params) as r1:
      2     print(r1.send_show_command('sh clock'))
----> 3     raise ValueError('Возникла ошибка')
      4

ValueError: Возникла ошибка
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
		
	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.telnet.close()
