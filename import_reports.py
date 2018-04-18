#!/usr/bin/env python
## -*- coding: utf-8 -*-
# 
# File: import_reports.py
# Author: Matthew A. Weidner <@jopawp>
# Date: 09/04/2016
# Descr: Imports sqlite3 database h1-reports.db from downloaded HackerOne
# 		 reports located in reports/
# 		 Use this to recreate the databse after schema modification.


import os
import sys
import json
import npyscreen
import sqlite3
import pdb
from subprocess import call

class AddressDatabase(object):
	def __init__(self, filename="h1-reports.db"):
		self.dbfilename = filename
		db = sqlite3.connect(self.dbfilename)
		c = db.cursor()
		c.execute(
				"CREATE TABLE IF NOT EXISTS reports\
						( record_internal_id INTEGER PRIMARY KEY, \
						report_id     TEXT, \
						created_at    TIME, \
						disclosed_at  TIME, \
						title         TEXT, \
						program       TEXT, \
						reporter      TEXT, \
						json          TEXT \
						)" \
						)
		db.commit()
		c.close()

	def add_record(self, report_id='', created='', disclosed='', title='', program='', reporter='', json_str=''):
		#print(report_id, date[:10], json_str)
		#input("Press Enter to continue...")
		title = title.strip()
		db = sqlite3.connect(self.dbfilename)
		c = db.cursor()
		c.execute('INSERT INTO reports(report_id, created_at, disclosed_at, title, program, \
			reporter, json) VALUES(?,?,?,?,?,?,?)', \
			(report_id, created, disclosed, title, program, reporter, json_str))
		db.commit()
		c.close()

if __name__ == '__main__':
	mydb = AddressDatabase()
	archive_dir = '/home/orion/bugbounty/h1/reports/'
	report_dir = archive_dir #+ 'new/'
	print('Adding reports from: ' + report_dir)
	for file_name in os.listdir(report_dir):
		if os.path.isfile(report_dir + file_name):
			f = open(report_dir + file_name)
			raw = f.read()
			if raw != '':
				j = json.loads(raw)
				if j['reporter'] is not None:
					rep = j['reporter']['username']
				else:
					rep = 'Unknown'
				#print('Adding ' + str(j['id']))
				mydb.add_record(report_id=str(j['id']), created=j['created_at'], \
						disclosed=j['disclosed_at'], title=j['title'],\
						program=j['team']['profile']['name'], \
						reporter=rep, json_str=raw)
	# find ./ -type f -size +0 -exec mv -t ../ {} +
	#call(['find', report_dir, '-type', 'f', '-size', '+0', '-exec', 'mv', \
		#	'-t', archive_dir, '{}', '+'])
