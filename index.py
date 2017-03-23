#!/usr/bin/python

# Import modules for CGI handling 
import cgi 
import cgitb
import csv
import subprocess
import os

# Create instance of FieldStorage 
# form = cgi.FieldStorage() 

# Get data from fields
# authkey = form.getvalue('authkey')

import sqlite3, time

con = sqlite3.connect("duty.sqlite", check_same_thread = False)
cur = con.cursor()

output = "<div style='font: comic sans'><h1>duty.py operations log</h1></div>"
output += "<table>"
output += "<tr><td>Date</td><td>Time</td><td>Incident Key</td><td>Action</td></tr>"

events = cur.execute("select * from operations order by epoch_time desc").fetchall()

for event in events:
    t = event[0]
    tt1 = time.strftime('%Y-%m-%d', time.localtime(t))
    tt2 = time.strftime('%H:%M:%S', time.localtime(t))
    k = event[1]
    s = event[2]
    ss = s.split(" ")[0]
    color = "white"
    if ss == "ACK":
        color = "#cea"
    if ss == "RECEIVED":
        color = "#ace"
    if ss == "ESCALATING":
        color = "#eca"

    output += "<tr style='margin: 0px; background-color: {4}'><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>".format(tt1, tt2, k, s, color)
    

output += "</table>"

print "Content-type:text/html\r\n\r\n"
print "<html><head><style>a { text-decoration: none; color: steelblue; } input { border: 1px solid grey; padding: 0.3em; margin: 0.3em; } .buttonadd { border-radius: 8px; background-color: #4CAF50; border: none; color: white; padding: 5px 12px; text-align: center; text-decoration: none; display: inline-block; font-size:16px; } body { padding: 1em; font-family: 'Ubuntu'} td { font-family: monospace; font-size: 1.5em; padding-right: 1em; padding-left: 1em; } .buttondel { border-radius: 8px; background-color: #f44336; border: none; color: white; padding: 5px 12px; text-align: center; text-decoration: none; display: inline-block; font-size:16px; } body { padding: 1em; } td { font-family: 'Ubuntu Mono', monospace; font-size: 1em; padding-right: 1em; padding-left: 1em; } table { border: 1px solid grey; padding: 1em; margin: 1em; } h2 { font-size: 0.9em; }</style><title>duty.py operations log</title></head></html>"
print "<body>{0}</body></html>".format(output)
