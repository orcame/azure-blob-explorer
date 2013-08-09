# !/usr/bin/python
# Filename: util.py

import time
from datetime import datetime

def format_time(timeStr):
	time= datetime.strptime(timeStr,'%a, %d %b %Y %H:%M:%S %Z')
	return time.strftime('%m/%d/%Y %H:%M %p')

def format_size(size,unit='auto'):
	units=['B','KB','MB','GB','TB']
	p=0
	while size>1024:
		if p==len(units)-1:
			break
		if units[p]==unit:
			break
		size = size/1024.0
		p+=1
	return str(round(size,2))+units[p] 