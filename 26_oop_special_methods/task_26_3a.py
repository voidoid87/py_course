# -*- coding: utf-8 -*-

'''
Задание 26.3a

Изменить класс IPAddress из задания 26.3.

Добавить два строковых представления для экземпляров класса IPAddress.
Как дожны выглядеть строковые представления, надо определить из вывода ниже:

Создание экземпляра
In [5]: ip1 = IPAddress('10.1.1.1/24')

In [6]: str(ip1)
Out[6]: 'IP address 10.1.1.1/24'

In [7]: print(ip1)
IP address 10.1.1.1/24

In [8]: ip1
Out[8]: IPAddress('10.1.1.1/24')

In [9]: ip_list = []

In [10]: ip_list.append(ip1)

In [11]: ip_list
Out[11]: [IPAddress('10.1.1.1/24')]

In [12]: print(ip_list)
[IPAddress('10.1.1.1/24')]

Для этого задания нет теста!
'''

class IPAddress:
	
	def __init__(self, addr_mask):
		try:
			self.ip, self.mask = addr_mask.split('/')
			self.mask = int(self.mask)
		except:
			print('Incorrect ip/mask')
		ip_list = self.ip.strip().split('.')
		if not len(ip_list)==4:
			raise ValueError('Incorrect IPv4 address')
		for octet in ip_list:
			if not(0<=int(octet)<=255):
				raise ValueError('Incorrect IPv4 address')
				break
		if not(8<=int(self.mask)<=32):
			raise ValueError('Incorrect mask')
			
	def __str__(self):
		return 'IP address {}/{}'.format(self.ip, self.mask)

	def __repr__(self):
		return "IP address ('{}/{}')".format(self.ip, self.mask)
		
if __name__== '__main__':
	ip1 = IPAddress('10.1.1.1/24')
	print(ip1)
