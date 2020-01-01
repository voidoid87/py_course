#!/usr/bin/env python3
import sqlite3
import re
import yaml
import re

def AddRowToTable(connection, query, row):
	try:
		connection.execute(query, row)
	except sqlite3.IntegrityError as e:
		print('While adding data ' + str(row) + ' the error occured', e)

def OpenConnectionToDB(dbName):
	conn = sqlite3.connect(dbName)
	return conn

def add_switches_data(fileyaml):
	switches = []
	with open(fileyaml, 'r') as f:
		raw_switches = yaml.safe_load(f)
	for i in raw_switches['switches'].keys():
		t = (i, raw_switches['switches'][i])
		switches.append(t)
	print('Adding data to SWITCHES table ...')
	query = 'INSERT into switches values (?, ?)'
	conn = OpenConnectionToDB('dhcp_snooping.db')
	for row in switches:
		AddRowToTable(conn,query,row)		
	conn.commit()
	conn.close()

def AddDataToDhcpTable(filenames):
	regex = re.compile(r'(\S+) +(\S+) +\d{5} +\S+ +(\d\d?) +(\S+)')
	data = []
	for files in filenames:
		host = files.split('_')[0]
		with open(files, 'r') as f:
			for line in f:
				match = re.search(regex, line)
				if type(match) == re.Match:
					t = []
					t = list(match.groups())
					t.append(host)
					t = tuple(t)
					data.append(t)
	conn = OpenConnectionToDB('dhcp_snooping.db')
	query = 'INSERT into dhcp values (?, ?, ?, ?, ?)'
	print('Adding data to DHCP table ...')
	for row in data:
		AddRowToTable(conn,query,row)		
	conn.commit()
	conn.close() 
		

if __name__ == '__main__':
	filenames = ['sw1_dhcp_snooping.txt', 'sw2_dhcp_snooping.txt', 'sw3_dhcp_snooping.txt']
	add_switches_data('switches.yml')
	conn = sqlite3.connect('dhcp_snooping.db')
#	for row in conn.execute('select * from switches'):
#		print(row)
	AddDataToDhcpTable(filenames)
#	for row in conn.execute('select * from dhcp'):
#		print(row)
