#!/usr/bin/python
# Filename: account.py
'''
maintance the accounts info of the command tool
accounts [-iolsd [id|prefix:]id_or_prefix]
	-i 	[[prefix:]prefix], show the infomation of accounts match the prefix value.
	-o 	[id:]id, connect the account by id.
	-l 	[[prefix:]prefix], list the accounts match the prefix value.
	-s 	[id:]id, save current account with id equals the specified value.
	-d 	[id:]id, delet the account with id equals the specified value.
'''
import os
import sys

from cmdparameter import (CmdParameter,CmdParameters)
from azurebe.client.storageclient import AccountInfo

class _Params(CmdParameters):
	def __init__(self,input=None):
		CmdParameters.__init__(self,option_default='i')
		self.id=CmdParameter()
		self.input=input

if sys.platform=='win32':
	CONFIG_PATH=os.environ["APPDATA"]+'\\azurebe\\accounts.config'
else:
	CONFIG_PATH='~/.azurebe/accounts.config'

def __read_config(id=None,prefix=None):
	'''
	read the config file. return the account list or a single account

	id:optional, if specified, return the account info by id, else return account list
	'''
	if not os.path.exists(CONFIG_PATH):
		return []
	cfg = open(CONFIG_PATH,'r')
	acs=[]
	try:
		lines=cfg.readlines()
		for line in lines:
			l = line.rstrip('\n')
			if l == '[account]':
				ac=AccountInfo()
				acs.append(ac)
			else:
				kv=l.split(':')
				n=kv[0]
				v=kv[1]
				if n=='id':
					ac.id=v
				elif n=='account_name':
					ac.account_name=v
				elif n=='account_key':
					ac.account_key=v
				elif n=='protocol':
					ac.protocol=v
				elif n=='host_base':
					ac.host_base=v

		if id:
			for a in acs:
				if a.id==id:
					return a
			else:
				return None
		elif prefix:
			acs = [a for a in acs if a.id.startswith(prefix)]
		return acs
	finally:
		cfg.close()

def __modify_config(configs,config,delete=False):
	if delete:
		configs=[c for c in configs if c.id != config.id]
	else:
		for idx,ac in enumerate(configs):
			if ac.id==config.id:
				configs[idx]=config
				break
		else:
			configs.append(config)
	return configs

def __save_config(client,id,delete=False):
	client.account_info.id=id

	if not os.path.exists(os.path.dirname(CONFIG_PATH)):
		os.makedirs(os.path.dirname(CONFIG_PATH))
	acs = __read_config()
	acs = __modify_config(acs,client.account_info,delete)
	
	lines=[]

	for ac in acs:
		lines.append('[account]')
		lines.append('id:'+ac.id)
		lines.append('account_name:'+ac.account_name)
		lines.append('account_key:'+ac.account_key)
		lines.append('protocol:'+ac.protocol)
		lines.append('host_base:'+ac.host_base)
	lines = [l+'\n' for l in lines]

	cfg = open(CONFIG_PATH,'w+')
	try:	
		cfg.writelines(lines)
	finally:
		cfg.close()

def __show_account(cmd,account):
	cmd.hightlight('===Account[id:%s]===' % account.id)
	cmd.info('\taccount_name:%s' % account.account_name)
	cmd.info('\taccount_key:%s' % account.account_key)
	cmd.info('\tprotocol:%s' % account.protocol)
	cmd.info('\thost_base:%s' % account.host_base)

def do_action(cmd,p):
	id=p.id.value
	o = p.option.value
	if o=='i':
		acs = __read_config(prefix=id)
		if type(acs)==list:
			for a in acs:
				__show_account(cmd,a)
		else:
			__show_account(cmd,ac)
	elif o=='o':
		if not id:
			raise Exception('the id of account can not be empty.use -l to list all accounts')
		else:
			acs=__read_config(id=id)
			if not acs:
				raise Exception('the account with id:%s not exists' % p.id.value)
			else:
				cmd.client.connect_stroage(acs.account_name,acs.account_key,acs.protocol,acs.host_base)
				cmd.client.account_info=acs
	elif o=='l':
		acs = __read_config(prefix=id)
		if acs:
			for a in acs:
				cmd.info('\t%s[id=%s]',a.account_name,a.id)
	elif o=='s':		
		if not cmd.client.account_info:
			raise Exception("current account is empty. use 'account -o' or 'connect' command to open one account.")
		if not id:
			id=cmd.client.account_info.id
		if not id:
			raise Exception('the id can not be empty.')
		else:
			__save_config(cmd.client,id,False)
	elif o=='d':
		if not id:
			id=cmd.client.account_info.id
		if not id:
			raise Exception('the id of account can not be empty.use -l to list all accounts')
		else:
			__save_config(cmd.client,id,True)
	else:
		raise Exception('unknown option -%s' % o)
