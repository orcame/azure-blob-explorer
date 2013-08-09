#!/usr/bin/python
# Filename: dir.py

'''
list blobs under current path.
	dir [prefix]
'''

import util
import string
from azure.storage import (Container,Blob)
from cmdparameter import (CmdParameter,CmdParameters)

class _Params(CmdParameters):
	def __init__(self):
		CmdParameters.__init__(self)
		self.prefix=CmdParameter()

def do_action(cmd,p):
	bc=cmd.client
	if bc.container:
		ls=bc.list_blobs(p.prefix.value)
	else:
		ls=bc.list_containers(p.prefix.value)
	cs=0 #coutainer count
	bs=0 #blob count
	ts=0 #total_size(blob)
	formatter='%s \t%s \t%s'
	path_idx=len(string.join(bc.paths,bc.path_separator))
	if path_idx:
		path_idx+=1
	for l in ls:
		if isinstance(l,Container):
			cs+=1
			size='<DIR>'
			name=l.name
		else:
			bs+=1
			size=l.properties.content_length
			ts+=size
			size=util.format_size(size)
			name=l.name[path_idx:]
		time=l.properties.last_modified
		time=util.format_time(time)
		cmd.info(formatter,time,size,name)
	cmd.hightlight('\tcontainer(s):%s\tblob(s):%s\tblob size:%s',cs,bs,util.format_size(ts))