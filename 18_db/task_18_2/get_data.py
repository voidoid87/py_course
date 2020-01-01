#!/usr/bin/env python3
import argparse
import sqlite3


def FetchAllDataFromTab(Connection, tabName):
	query = 'select * from ' + tabName
	print('dhcp table has following records:')
	print('-'*63)
	for row in connection.execute(query):
		print(row)
	print('-'*63)

def FetchDataFromTab(Connection, tabName, param):
	query = 'select * from ' + tabName + ' where '
	
		
def ConnectToDatabase(dbName):
	con = sqlite3.connect(dbName)
	return con

parser = argparse.ArgumentParser(description = 'Get data from db script')
parser.add_argument('key',
					choices = ['mac', 'ip', 'vlan', 'interface', 'switch'],
					help='host key (parameter) to search', required = False)
parser.add_argument('val', action = 'store')

if __name__=='__main__':
	dbName = 'dhcp_snooping.db'
	tabName = 'dhcp'
	args = parser.parse_args()
    #print(args)
