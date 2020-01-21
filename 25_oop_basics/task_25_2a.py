# -*- coding: utf-8 -*-

'''
Задание 25.2a

Скопировать класс CiscoTelnet из задания 25.2 и изменить метод send_show_command добавив два параметра:

* parse - контролирует то, будет возвращаться обычный вывод команды или список словарей, полученные после обработки с помощью TextFSM. При parse=True должен возвращаться список словарей, а parse=False обычный вывод
* templates - путь к каталогу с шаблонами



Пример создания экземпляра класса:

In [1]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [2]: from task_25_2a import CiscoTelnet

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_show_command:
In [4]: r1.send_show_command('sh ip int br', parse=False)
Out[4]: 'sh ip int br\r\nInterface                  IP-Address      OK? Method Status                Protocol\r\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \r\nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \r\nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \r\nEthernet0/3                192.168.130.1   YES NVRAM  up                    up      \r\nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \r\nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \r\nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      \r\nLoopback0                  10.1.1.1        YES NVRAM  up                    up      \r\nLoopback55                 5.5.5.5         YES manual up                    up      \r\nR1#'

In [5]: r1.send_show_command('sh ip int br', parse=True)
Out[5]:
[{'intf': 'Ethernet0/0',
  'address': '192.168.100.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/1',
  'address': '192.168.200.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/2',
  'address': '190.16.200.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/3',
  'address': '192.168.130.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/3.100',
  'address': '10.100.0.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/3.200',
  'address': '10.200.0.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/3.300',
  'address': '10.30.0.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Loopback0',
  'address': '10.1.1.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Loopback55',
  'address': '5.5.5.5',
  'status': 'up',
  'protocol': 'up'}]
'''

import telnetlib
import textfsm

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
				


		
if __name__ == '__main__':
	
	r1_params = {
				'ip': '192.168.100.1',
				'username': 'cisco',
				'password': 'cisco',
				'secret': 'cisco'}	
					
	r1 = CiscoTelnet(**r1_params)	
	print(r1.send_show_command('sh ip int br', True))	
		
		
