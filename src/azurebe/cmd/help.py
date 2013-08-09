#!/usr/bin/python
# Filename: help.py

'''
Got the help info of command
'''

import azurebe.cmd as cmds
from cmdparameter import (CmdParameter,CmdParameters)

class _Params(CmdParameters):
	def __init__(self):
		CmdParameters.__init__(self)
		self.cmdname=CmdParameter()
		self.wordchars=self.alphanum
		self.whitespace_split=True

def do_action(cmd,p):
	if not p.cmdname.value:
		cmd.write_line('command list:')
		for cmd_name in cmds.__all__:
			command = getattr(cmds,cmd_name)
			if 'do_action' in dir(command):
				cmd.write_line('\t%s',cmd_name)
	else:
		cmd.help(p.cmdname.value)