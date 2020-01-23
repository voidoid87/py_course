# -*- coding: utf-8 -*-

'''
Задание 26.1a

В этом задании надо сделать так, чтобы экземпляры класса Topology были итерируемыми объектами.
Основу класса Topology можно взять из любого задания 25.1x или задания 26.1.

После создания экземпляра класса, экземпляр должен работать как итерируемый объект.
На каждой итерации должен возвращаться кортеж, который описывает одно соединение.
Порядок вывода соединений может быть любым.


Пример работы класса:

In [1]: top = Topology(topology_example)

In [2]: for link in top:
   ...:     print(link)
   ...:
(('R1', 'Eth0/0'), ('SW1', 'Eth0/1'))
(('R2', 'Eth0/0'), ('SW1', 'Eth0/2'))
(('R2', 'Eth0/1'), ('SW2', 'Eth0/11'))
(('R3', 'Eth0/0'), ('SW1', 'Eth0/3'))
(('R3', 'Eth0/1'), ('R4', 'Eth0/0'))
(('R3', 'Eth0/2'), ('R5', 'Eth0/0'))


Проверить работу класса.
'''

topology_example = {('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
                    ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
                    ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
                    ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
                    ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
                    ('R3', 'Eth0/2'): ('R5', 'Eth0/0'),
                    ('SW1', 'Eth0/1'): ('R1', 'Eth0/0'),
                    ('SW1', 'Eth0/2'): ('R2', 'Eth0/0'),
                    ('SW1', 'Eth0/3'): ('R3', 'Eth0/0')}

class Topology:
	def __init__(self, topology_dict):
		self.topology = self._normalize(topology_dict)

	def _normalize(self, topology_dict):
		normal_dict = {}
		for key, val in topology_dict.items():
			if not (normal_dict.get(key)) and not (normal_dict.get(val)==key):
				normal_dict[key] = val
		return normal_dict
	
	def delete_link(self, key, val):
		if self.topology.get(key):
			del  self.topology[key]
		elif self.topology.get(val) == key:
			del  self.topology[val]
		else:
			print('Такого соединения нет')
	
	def delete_node(self, node):
		deleted = False
		d = self.topology.copy()
		for key, val in d.items():
			if (node in key) or (node in val):
				del self.topology[key]
				deleted = True
		if not deleted:
			print('Такого устройства нет')
			
	def add_link(self, key, val):
		if self.topology.get(key) == val:
			print("Такое соединение существует")
		elif self.topology.get(key) or self.topology.get(val):
			print("Cоединение с одним из портов существует")
		else:
			self.topology[key] = val
			
	def __add__(self, other_topology):
		d = Topology(self.topology) 
		d.topology.update(other_topology.topology)
		return d
	
	def __iter__(self):
		return iter(self.topology.values())

if __name__ == '__main__':
		pass
