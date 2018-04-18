#!/usr/bin/env python
import os
import json
import pprint
import re

# sort in place:
# ut.sort(key=lambda x: x.count, reverse=True)
# 
# count is an attribute of every object in the list.

class h1_report():
    filename = ''
    reporter = ''
    program = ''
    bounty = '0'
    vuln_types = []

    def __init__(self, filename, reporter, program, bounty, vuln_types):
        self.filename = filename
        self.reporter = reporter
        self.program = program
        self.bounty = bounty
        self.vuln_types = vuln_types

reports = []

print('Loading data...')
for i in os.listdir(os.getcwd()+'/reports/'):
    if i.endswith(".json"): 
        f = open(os.getcwd() + '/reports/' + i)
        j = f.read()
        f.close()
        d = json.loads(j)
        if d['has_bounty?'] == True:
            try:
                # Calculate bounty using bounty_amount field
                a = d['bounty_amount']
                b = re.sub('\.0','',a)
                bounty = int(b)
                #print('A: ' + repr(a))
                #print('B: ' + repr(b))
                #print('Bounty: ' + repr(bounty))
            except:
                bounty = 0
        else:
            bounty = 0
        try:
            reporter = d['reporter']['username']
        except:
            reporter = 'No reporter listed'
        vuln_types = d['vulnerability_types']
        vtypes = []
        for vuln_type in vuln_types:
            vtypes.append([repr(vuln_type['id']), vuln_type['name']])
        reports.append(h1_report(i,reporter, \
                d['team']['profile']['name'], bounty, vtypes))
        continue
    else:
        continue

#print('Sorting by bounty...')
#reports.sort(key=lambda x: x.bounty, reverse=True)

#print('Sorting by program...')
#reports.sort(key=lambda x: x.program, reverse=True)

#print('Sorting by reporter...')
#reports.sort(key=lambda x: x.reporter, reverse=True)

bounties = {}
programs = {}
reporters = {}
for report in reports:
    if report.reporter in bounties:
        bounties[report.reporter] = bounties[report.reporter] + report.bounty
    else:
        bounties[report.reporter] = report.bounty

    if report.program in programs:
        programs[report.program] = programs[report.program] + 1
    else:
        programs[report.program] = 1

    if report.reporter in reporters:
        reporters[report.reporter] = reporters[report.reporter] + 1
    else:
        reporters[report.reporter] = 1
        
    #print(report.filename)
    #print(report.reporter)
    #print(report.program)
    #print(report.bounty)
    #pprint.pprint(report.vuln_types)
    #print('*'*30)

pprint.pprint(sorted(bounties.items(), key=lambda x: x[1]))
pprint.pprint(sorted(programs.items(), key=lambda x: x[1]))
pprint.pprint(sorted(reporters.items(), key=lambda x: x[1]))
