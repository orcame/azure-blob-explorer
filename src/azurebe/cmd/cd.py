#!/usr/bin/python
# Filename: cd.py
'''
change the parent directory
	cd dictname
	cd ..
'''

from cmdparameter import (CmdParameter,CmdParameters)

class _Params(CmdParameters):
	def __init__(self):
		CmdParameters.__init__(self)
		self.wordchars=self.alphanum+'-:?.'
		self.whitespace_split=True

def do_action(cmd,p):
	if p.argvs:
		p=p.argvs[0]
		ps=p.split(cmd.client.path_separator)
		ps=[p for p in ps if p]
		for p in ps:
			if p=='..':
				if cmd.client.paths:
					cmd.client.pop_path()
				else:
					cmd.client.set_container(None)
					cmd.client.path=[]
				continue
			if not cmd.client.container:
				cmd.client.set_container(p)
			else:
				cmd.client.append_path(p)
