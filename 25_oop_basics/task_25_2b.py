# -*- coding: utf-8 -*-

'''
Задание 25.2b

Скопировать класс CiscoTelnet из задания 25.2a и добавить метод send_config_commands.


Метод send_config_commands должен уметь отправлять одну команду конфигурационного режима или список команд.
Метод должен возвращать вывод аналогичный методу send_config_set у netmiko (пример вывода ниже).

Пример создания экземпляра класса:
In [1]: from task_25_2b import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_config_commands:

In [5]: r1.send_config_commands('logging 10.1.1.1')
Out[5]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#logging 10.1.1.1\r\nR1(config)#end\r\nR1#'

In [6]: r1.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255'])
Out[6]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#interface loop55\r\nR1(config-if)#ip address 5.5.5.5 255.255.255.255\r\nR1(config-if)#end\r\nR1#'

'''

import telnetlib
import textfsm
import time

class CiscoTelnet:
	def __init__(self, ip, username, password, secret):
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
				

	def send_config_commands(self, commands):
		if type(commands)==str:
			self._write_line('configure terminal')
			self._write_line(commands)
			self._write_line('end')
		elif type(commands) == list:
			self._write_line('configure terminal')
			for command in commands:
				self._write_line(command)
			self._write_line('end')
		time.sleep(1)
		return(self.telnet.read_very_eager().decode('utf-8'))
		
if __name__ == '__main__':
	
	r1_params = {
				'ip': '192.168.100.1',
				'username': 'cisco',
				'password': 'cisco',
				'secret': 'cisco'}	
					
	r1 = CiscoTelnet(**r1_params)	
	print(r1.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255']))	
		
