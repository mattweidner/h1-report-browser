#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# File: h1-browser.py
# Author: Matthew A. Weidner <@jopawp>
# Date: 09/04/2016
# Descr: Offline HackerOne report browser using an offline cache contained
# 		 in a sqlite3 database. Ncurses interface.

import os
import sys
import pdb
import sys
import time
import json
import curses
import sqlite3
import npyscreen

class ReportDatabase(object):
	def __init__(self, filename="h1-reports.db"):
		self.dbfilename = filename

	def list_all_reports(self, ):
		db = sqlite3.connect(self.dbfilename)
		c = db.cursor()
		c.execute('SELECT * from reports ORDER BY disclosed_at DESC')
		reports = c.fetchall()
		c.close()
		return reports

	def get_report(self, report_id):
		db = sqlite3.connect(self.dbfilename)
		c = db.cursor()
		c.execute('SELECT * from reports WHERE report_id=?', (report_id,))
		reports = c.fetchall()
		c.close()
		return reports[0]

class ReportList(npyscreen.MultiLineAction):
	def __init__(self, *args, **keywords):
		super(ReportList, self).__init__(*args, **keywords)
		self.add_handlers({
			#curses.KEY_ENTER: self.dummy,
			#curses.ascii.CR: self.dummy,
			#curses.ascii.NL: self.dummy,
			"Q": self.quit,
			"q": self.quit
			})

	def dummy(self, *args, **keywords):
		npyscreen.notify('Key pressed: ' + str(args))
		time.sleep(1)
		pass

	def quit(self, *args, **keywords):
		sys.exit()

	def actionHighlighted(self, act_on_this, keypress):
		# this passes the report_id to the other form.
		self.parent.parentApp.getForm('READ').value=act_on_this[1]
		# Select report from database and add it to the 
		# ReportView form.
		self.parent.parentApp.switchForm('READ')

	def display_value(self, vl):
		return "%s  %s  %s" % (vl[1], vl[3], vl[4])

class ReportView(npyscreen.MultiLineAction):
	def __init__(self, *args, **keywords):
		super(ReportView, self).__init__(*args, **keywords)
		self.add_handlers({
			curses.KEY_ENTER: self.quit,
			curses.ascii.CR: self.quit,
			curses.ascii.NL: self.quit,
			"Q": self.quit,
			"q": self.quit
			})

	def dummy(self, *args, **keywords):
		npyscreen.notify('Key pressed: ' + str(args))
		time.sleep(1)
		pass

	def quit(self, *args, **keywords):
		self.parent.parentApp.switchFormPrevious()

	def display_value(self, vl):
		return "%s" % (vl[0])

class FmReportView(npyscreen.FormMutt):
	MAIN_WIDGET_CLASS = ReportView
	def beforeEditing(self):
		npyscreen.notify('Generating report.', self.parentApp.app_title)
		self.update_list()

	def update_list(self):
		self.wStatus1.value = 'Report ' + self.value + ' '
		report = self.parentApp.myDB.get_report(self.value)
		j = json.loads(report[7])
		self.wMain.values = self.format_report(j)
		self.wMain.display()

	def split_maxlen(self, maxlen, line, lines, prepend=''):
		# splits a string of text on spaces, not to exceed maxlen
		# inserts each line as single dimension list into lines.
		#line = line.replace('\n', '')
		#' '.join(line.split())
		maxlen = maxlen - len(prepend)
		while len(line) > maxlen:
			spaces = [0]
			for i, letter in enumerate(line):
				if letter == ' ':
					#print(i, letter)
					spaces.append(i)
			#spaces = [i for i, letter in enumerate(line) if letter == ' ']
			#print(spaces)

			split_pos = [i for i, space in enumerate(spaces) if space <= maxlen]
			#npyscreen.notify(repr(split_pos) + "\n" + repr(spaces), 'SpaceSplits!')
			#time.sleep(1)
			#pdb.set_trace()
			#input(">> ")
			if len(split_pos) > 0:
				if spaces[split_pos[-1]] == 0:
					str=line[0:maxlen]
					spaces[split_pos[-1]] = maxlen
				else:
					str=line[0:spaces[split_pos[-1]]]
			else:
				str = ""
			t = str.strip()
			#print('line: ', t)
			if t is not '':
				lines.append([prepend + str.strip()])
			if len(split_pos) > 0:
				line=line[spaces[split_pos[-1]]:]
			else:
				line = ""
			#input(">> ")
		if len(line) > 0:
			lines.append([prepend + line.strip()])
	

	def format_report(self, j):
		#maxlen = self.columns - 1
		maxlen = 79
		multiline_values = []
		report_id = j['id']
		try:
			if j['reporter'] is not None:
				reporter = j['reporter']['username']
			else:
				reporter = 'Unknown'
				raise ValueError('Reporter field is None.')
		except:
			reporter = 'Unknown'
		url = j['url']
		created_at = j['created_at']
		disclosed_at = j['disclosed_at']
		title = j['title']
		team_id = j['team']['id']
		team = j['team']['profile']['name']
		try:
			vuln_types = j['vulnerability_types']
		except:
			try:
				vuln_types = [j['weakness']]
			except:
				vuln_types = [{'id':9999, 'name':'Unknown' }]
				vuln_types['name'] = 'Unknown'
		report = j['vulnerability_information']
		if j['has_bounty?'] == True:
			try:
				bounty = j['formatted_bounty']
			except:
				bounty = 'Has bounty, but unable to determine amount'
		else:
			bounty = "No bounty."

		multiline_values.append(['Bounty Program: ' + team + ' (' + repr(team_id) + ')'])
		multiline_values.append(['Disclosed: ' + disclosed_at])
		multiline_values.append(['Created: ' + created_at])
		multiline_values.append(['Report url: ' + url])
		multiline_values.append([' '])
		multiline_values.append(['Bounty: ' + bounty])
		multiline_values.append([' '])
		multiline_values.append(['Vulnerability Types:'])
		for vuln_type in vuln_types:
			multiline_values.append(['  ' + '(' + repr(vuln_type['id']) + ')' + vuln_type['name']])
		multiline_values.append([' '])
		multiline_values.append(['Report by <' + reporter + '> on ' + created_at])
		multiline_values.append([' '])
		tmp_list = [s.strip() for s in report.splitlines()]
		for line in tmp_list:
			self.split_maxlen(maxlen, line, multiline_values)
		activities = j['activities']
		multiline_values.append([' '])
		multiline_values.append([' '])
		multiline_values.append(['Comments:'])
		for i, a in enumerate(activities):
			activity_type = a['type'][12:]
			try:
				m = a['message']
			except:
				m = None
			if m is None:
				continue
			if len(m) > 0:
				if a['actor'] is None:
					user = 'Unknown'
				else:
					try:
						user = a['actor']['username']
					except:
						try:
							user = a['actor']['profile']['name']
						except:
							user = 'UNKNOWN'
				multiline_values.append(['(Event ' + repr(i) + ') ' + activity_type + ' ' + '-'*((maxlen)-len(activity_type))])
				multiline_values.append([' '])
				multiline_values.append(['  <' + user + '>' + '  ' + a['created_at']])
				multiline_values.append([' '])
				self.split_maxlen(maxlen, m, multiline_values, prepend='    ')
				#multiline_values.append(['    ' + m])
				multiline_values.append([' '])
		return multiline_values
	

class FmReportSelect(npyscreen.FormMutt):
	MAIN_WIDGET_CLASS = ReportList
	def update_list(self):
		self.wMain.values = self.parentApp.myDB.list_all_reports()
		self.wMain.display()

class TestApp(npyscreen.NPSAppManaged):
	reports = []
	def onStart(self):
		self.app_title = 'H1 Report Browser'
		self.myDB = ReportDatabase()
		self.addForm('MAIN', FmReportSelect)
		npyscreen.notify('Generating list of reports.', self.app_title)
		self.getForm('MAIN').update_list()
		self.getForm('MAIN').wStatus1.value = self.app_title
		self.getForm('MAIN').wStatus2.value = 'Press Enter to read the highlighted report. Q or q to quit.'
		self.addForm('READ', FmReportView)
		self.getForm('READ').wStatus1.value = 'Report '
		self.getForm('READ').wStatus2.value = 'Press q, Q, or Enter to return to report list. '
		self.getForm('READ').wMain.autowrap = True

# sort a list of dictionaries by a key
# newlist = sorted(list_to_be_sorted, key=lambda k: k['date']) 

if __name__ == "__main__":
	App = TestApp()
	App.run()
