#!/usr/bin/env python

import sqlite3
import os
import sys

def db_exists(db_name):
	return os.path.exists(db_name)
	
def create_db(db_name, schema_file):
	if db_exists(db_name):
		print('Database already exists')
	else:
		print('Creating database...')
		conn = sqlite3.connect(db_name)
		with open(schema_file, 'r') as f:
			schema = f.read()
			conn.executescript(schema)
	
if __name__ == '__main__':
	db_name = 'dhcp_snooping.db'
	schema_file = 'dhcp_snooping_schema.sql'
	create_db(db_name, schema_file)
