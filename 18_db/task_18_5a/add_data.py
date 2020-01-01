#!/usr/bin/env python3
import sqlite3
import re
import yaml
import re
from datetime import timedelta, datetime


def DeleteObsoleteData(conn, days):
	now = datetime.today().replace(microsecond=0)
	obdate = now - timedelta(days=days)
	query = 'select * from dhcp'
	cursor = conn.cursor()
	result = cursor.execute(query)
	print('Deleting obsolete data...')
	for row in result:
		if str(row[-1])<= str(obdate):
			conn.executescript('delete {} from dhcp'.format(row))
	
	 
	
def AddRowToTable(connection, query, row):
	try:
		connection.execute(query, row)
	except sqlite3.IntegrityError as e:
		print('While adding data ' + str(row) + ' the error occured', e)

def OpenConnectionToDB(dbName):
	conn = sqlite3.connect(dbName)
	return conn

def add_switches_data(conn, fileyaml):
	switches = []
	with open(fileyaml, 'r') as f:
		raw_switches = yaml.safe_load(f)
	for i in raw_switches['switches'].keys():
		t = (i, raw_switches['switches'][i])
		switches.append(t)
	print('Adding data to SWITCHES table ...')
	query = 'INSERT into switches values (?, ?)'
	for row in switches:
		AddRowToTable(conn,query,row)		
	conn.commit()


def MarkDataInactive(conn, switch):
	query = "update dhcp set active = 0 where switch = '{}'".format(switch)
	conn.executescript(query)
	

def AddDataToDhcpTable(conn, filenames):
	regex = re.compile(r'(\S+) +(\S+) +\d{5} +\S+ +(\d\d?) +(\S+)')
	print('Adding data to DHCP table ...')
	for files in filenames:
		data = []
		host = files.split('/')[-1].split('_')[0]
		with open(files, 'r') as f:
			for line in f:
				match = re.search(regex, line)
				if type(match) == re.Match:
					t = []
					t = list(match.groups())
					t.append(host)
					t.append(1)
					t = tuple(t)
					data.append(t)
		MarkDataInactive(conn, host)
		query = "REPLACE into dhcp values (?, ?, ?, ?, ?, ?, '2019-05-11 11:11:11')"
		for row in data:
			AddRowToTable(conn,query,row)		
		conn.commit() 
		

if __name__ == '__main__':
	dbName = 'dhcp_snooping.db'
	#filenames = ['sw1_dhcp_snooping.txt', 'sw2_dhcp_snooping.txt', 'sw3_dhcp_snooping.txt','new_data/sw1_dhcp_snooping.txt', 'new_data/sw2_dhcp_snooping.txt', 'new_data/sw3_dhcp_snooping.txt']
	filenames = ['new_data/sw1_dhcp_snooping.txt', 'new_data/sw2_dhcp_snooping.txt', 'new_data/sw3_dhcp_snooping.txt']
	conn = OpenConnectionToDB(dbName)
	add_switches_data(conn, 'switches.yml')

	for row in conn.execute('select * from switches'):
		print(row)
	AddDataToDhcpTable(conn, filenames)
	for row in conn.execute('select * from dhcp'):
		print(row)
	DeleteObsoleteData(conn, 7)
	#for row in conn.execute('select * from dhcp'):
	#	print(row)
	conn.close()
