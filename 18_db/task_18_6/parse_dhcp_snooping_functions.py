import os
import sqlite3
import yaml
import re

def OpenConnectionToDB(db_name):
	conn = sqlite3.connect(db_name)
	return conn

def db_exists(db_name):
	return os.path.exists(db_name)
	
def create_db(db_file, schema_file):
	if db_exists(db_file):
		print('Database already exists')
	else:
		conn = OpenConnectionToDB(db_file)
		with open(schema_file, 'r') as f:
			schema = f.read()
			conn.executescript(schema)
	conn.close()

def add_data_switches(db_file, files_list):
	switches = []
	for yaml_file in files_list:
		with open(yaml_file, 'r') as f:
			raw_switches = yaml.safe_load(f)
		for i in raw_switches['switches'].keys():
			t = (i, raw_switches['switches'][i])
			switches.append(t)
		query = 'INSERT into switches values (?, ?)'
		conn = OpenConnectionToDB(db_file)
		for row in switches:
			AddRowToTable(conn,query,row)		
		conn.commit()
	conn.close()
	
def AddRowToTable(connection, query, row):
	try:
		connection.execute(query, row)
	except sqlite3.IntegrityError as e:
		print('While adding data ' + str(row) + ' the error occured', e)


def add_data(db_file, filenames):
	conn = OpenConnectionToDB(db_file)
	regex = re.compile(r'(\S+) +(\S+) +\d{5} +\S+ +(\d\d?) +(\S+)')
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
		query = "REPLACE into dhcp values (?, ?, ?, ?, ?, ?, datetime('now'))"
		for row in data:
			AddRowToTable(conn,query,row)		
		conn.commit() 
	conn.close()
		
def get_data(db_file, key = None, val = None):
	conn = OpenConnectionToDB(db_file)
	nonact = []
	if key and val:
		query = 'select * from dhcp where ' + key + ' = ' + "'{}'".format(val)
	else:
		query = 'select * from dhcp'
	print('\nActive records:')
	print('-'*63)
	for row in conn.execute(query):
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
	conn.commit()
			
def MarkDataInactive(conn, switch):
	query = "update dhcp set active = 0 where switch = '{}'".format(switch)
	conn.executescript(query)
	conn.commit()
	
