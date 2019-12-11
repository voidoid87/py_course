# -*- coding: utf-8 -*-
'''
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Дополнить скрипт:
- Запросить у пользователя ввод номера VLAN.
- Выводить информацию только по указанному VLAN.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''
lans=[]

with open('CAM_table.txt','r') as f:
	for line in f:
		if(line.strip()[0:2].isdigit()):
			lans.append(line.strip())
issorted = False
while not issorted:
	for i in range(len(lans)-2):
		num1 = int(lans[i].strip()[0:4])
		num2 = int(lans[i+1].strip()[0:4])
		if num1>num2:
			cash = lans[i+1]
			lans[i+1] = lans[i]
			lans[i] = cash
			break
	else:
		issorted = True
		
inp = input('Enter vlan number: ')
if inp.strip().isdigit():
	inp = int(inp)
	for line in lans:
		if inp == int(line[0:4].strip()):
			print(line)
