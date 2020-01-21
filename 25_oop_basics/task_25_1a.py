# -*- coding: utf-8 -*-

'''
Задание 25.1a

Скопировать класс Topology из задания 25.1 и изменить его.

Если в задании 25.1 удаление дублей выполнялось в методе __init__,
надо перенести функциональность удаления дублей в метод _normalize.

При этом метод __init__ должен выглядеть таким образом:
'''

class Topology:
	def __init__(self, topology_dict):
		self.topology = self._normalize(topology_dict)

	def _normalize(self, topology_dict):
		normal_dict = {}
		for key, val in topology_dict.items():
			if not (normal_dict.get(key)) and not (normal_dict.get(val)==key):
				normal_dict[key] = val
		return normal_dict


topology_example = {('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
                    ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
                    ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
                    ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
                    ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
                    ('R3', 'Eth0/2'): ('R5', 'Eth0/0'),
                    ('SW1', 'Eth0/1'): ('R1', 'Eth0/0'),
                    ('SW1', 'Eth0/2'): ('R2', 'Eth0/0'),
                    ('SW1', 'Eth0/3'): ('R3', 'Eth0/0')}

if __name__ == '__main__':
	t = Topology(topology_example)
	print(t.topology)	
