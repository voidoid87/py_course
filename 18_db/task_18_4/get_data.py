#!/usr/bin/env python3

import sqlite3
from sys import argv

allowed_args = ['mac', 'ip', 'vlan', 'interface', 'switch']

def FetchDataFromTab(connection, tabName, key = None, val = None):
	nonact = []
	if key and val:
		query = 'select * from ' + tabName + ' where ' + key + ' = ' + "'{}'".format(val)
		print('Information about switches with following params: ' + key + ' ' + val)
	else:
		query = 'select * from ' + tabName
		print('dhcp table has following records:')
	print('\nActive records:')
	print('-'*63)
	for row in connection.execute(query):
		if row[-1]:
			print(row)
		else:
			nonact.append(row)
	print('-'*63)
	if nonact:
		print('\nNon-active records:')
		print('-'*63)
		for row in nonact:
			print(row)
		print('-'*63)
		
def ConnectToDatabase(dbName):
	con = sqlite3.connect(dbName)
	return con



if __name__=='__main__':
	dbName = 'dhcp_snooping.db'
	tabName = 'dhcp'
	conn = ConnectToDatabase(dbName)
	if len(argv)==2 or len(argv)>3:
		print('Please, enter zero or two arguments')
	elif len(argv)==3:
		if not argv[1] in allowed_args:
			print('Entered parameter is not supported')
			print('Allowed parameters: mac, ip, vlan, interface, switch')
		else:
			FetchDataFromTab(conn, tabName, argv[1], argv[2])
	elif len(argv)==1:
		FetchDataFromTab(conn, tabName)
		
