# -*- coding: utf-8 -*-

'''
Задание 26.3

В этом задании необходимо создать класс IPAddress.

При создании экземпляра класса, как аргумент передается IP-адрес и маска,
а также выполняется проверка корректности адреса и маски:
* Адрес считается корректно заданным, если он:
   - состоит из 4 чисел разделенных точкой
   - каждое число в диапазоне от 0 до 255
* маска считается корректной, если это число в диапазоне от 8 до 32 включительно

Если маска или адрес не прошли проверку, необходимо сгенерировать исключение ValueError с соответствующим текстом (смотри вывод ниже).

Также, при создании класса, должны быть созданы два атрибута экземпляра: ip и mask, в которых содержатся адрес и маска, соответственно.

Пример создания экземпляра класса:
In [1]: ip = IPAddress('10.1.1.1/24')

Атрибуты ip и mask
In [2]: ip1 = IPAddress('10.1.1.1/24')

In [3]: ip1.ip
Out[3]: '10.1.1.1'

In [4]: ip1.mask
Out[4]: 24

Проверка корректности адреса (traceback сокращен)
In [5]: ip1 = IPAddress('10.1.1/24')
---------------------------------------------------------------------------
...
ValueError: Incorrect IPv4 address

Проверка корректности маски (traceback сокращен)
In [6]: ip1 = IPAddress('10.1.1.1/240')
---------------------------------------------------------------------------
...
ValueError: Incorrect mask

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
		
