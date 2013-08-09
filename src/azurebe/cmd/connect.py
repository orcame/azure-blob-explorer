#!/usr/bin/python
# Filename: cd.py
'''
connect to a storage account.

	connect account_name account_key [protocol] [host_base]
	
		[protocol]:default 'http'
		[host_base]:default '.blob.core.windows.net'

	after connect to a storage account ,you can use "account" command to save it
'''
from cmdparameter import (CmdParameter,CmdParameters)

class _Params(CmdParameters):
	def __init__(self):
		CmdParameters.__init__(self)
		self.account_name=CmdParameter()
		self.account_key=CmdParameter()
		self.protocol=CmdParameter(optional=True,default_value='http')
		self.host_base=CmdParameter(optional=True,default_value='.blob.core.windows.net')
		

def do_action(cmd,p):
	cmd.client.connect_stroage(p.account_name.value,p.account_key.value,p.protocol.value,p.host_base.value)
	
