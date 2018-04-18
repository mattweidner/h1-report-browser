#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# 
# File: h1-dl-reports.py
# Author: Matthew A. Weidner <@jopawp>
# Date: 09/04/2016
# Descr: Download publicly disclosed HackerOne reports for offline reading.
# 		 Now with a small, random courtesy delay between report requests!
# 		 Depends on curl for download.

import os
import sys
import json
import httplib2
import subprocess
from time import sleep
from time import time
from urllib2 import urlopen
from random import randint

G = '\033[92m' #green
Y = '\033[93m' #yellow
B = '\033[94m' #blue
R = '\033[91m' #red
W = '\033[0m'  #white

reports = os.path.join(os.getcwd(),"reports")
new_reports = os.path.join(reports, "new")

def go_curl(cmd):
	o = subprocess.check_output(cmd,shell=True)
	try:
		json_str = json.loads(o)
		return json_str
	except:
		return None

def get_report_list():
	print B + '[?] Downloading list of public disclosures...' + W
	return go_curl('curl -s -XGET "http://h1.nobbd.de/programs.json"')

def get_report_list_from_file():
	f = open('nobbd_report_links.json', 'r')
	d = f.read()
	return json.loads(d)

def quit():
	sys.exit()

def banner():
	print G + '      __  _____   ____                        __    '
	print '     / / / <  /  / __ \___  ____  ____  _____/ /______'
	print '    / /_/ // /  / /_/ / _ \/ __ \/ __ \/ ___/ __/ ___/'
	print '   / __  // /  / _, _/  __/ /_/ / /_/ / /  / /_(__  )'
	print '  /_/ /_//_/  /_/ |_|\___/ .___/\____/_/   \__/____/'
	print '                        /_/  Downloader             ' + W
	print ''
	print R + "       H1 Reports: Leech H1 disclosed reports" + W
	print Y + "             Matthew A. Weidner @jopawp" + W
	print ""
	print B + "[?] Random courtesy delay of 1-5 seconds between requests." + W
def main():
	banner()
	report_list = get_report_list()
	print(B + '[?] Processing report list.' + W)
	for report in report_list:
		report_id = str(report[4])
		file_name = reports + report_id + '.json'
		new_file_name = os.path.join(new_reports, report_id + ".json")
		if (os.path.isfile(file_name) is not True) and (os.path.isfile(new_file_name) is not True):
			print G + "[+] " + B + "Downloading new report: " \
					+ str(report_id) + W

			cmd = 'curl -s -A "H1 Report Leecher, now with polite random delay! ;-)" -XGET "https://hackerone.com/reports/' \
					+ report_id + '.json" > ' + new_file_name
			go_curl(cmd)
			delay = randint(0,4) + 1
			sleep(delay)
			# raw_input('Press Enter to continue...')
	print(G + '[+] Done.' + W)
if __name__ == "__main__":
	main()
