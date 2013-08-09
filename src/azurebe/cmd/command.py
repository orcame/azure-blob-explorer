#!/usr/bin/python
# Filename: command.py

import shlex
import types
import string

import azurebe.cmd as cmds
from azurebe.client import *
from azurebe.cmd.console import Console
from azurebe.client.blobclient import BlobClient
from azurebe.cmd.cmdparameter import CmdParameters

class Command:
	
	def __init__(self):
		self.client=BlobClient()
		self.console=Console()

	def __get_cmd_name(self,input):
		if not input:
			return None
		else:
			s=shlex.shlex(input,posix=True)
			return s.next()

	def __get_cmd(self,cmd_name):
		try:
			cmd = getattr(cmds,cmd_name)
			if type(cmd)==types.ModuleType and 'do_action' in dir(cmd):
				return cmd
			else:
				raise Exception('%s is not recognized as a command'%cmd_name)
		except:
			raise Exception('%s is not recognized as a command'%cmd_name)
	
	def __help(self,cmd):
		if cmd.__doc__:
			self.write_line(cmd.__doc__)
		else:
			self.warning('no document for command.')

	def __call_cmd(self,input):
		cmd_name=self.__get_cmd_name(input)
		if not cmd_name:
			pass
		else:
			cmd=self.__get_cmd(cmd_name)
			input = input[len(cmd_name):]
			if '_Params' in dir(cmd):
				p=cmd._Params()
			else:
				p=CmdParameters()
			p.generate(input)
			if p.option.value=='?':
				self.__help(cmd)
			else:
				cmd.do_action(self,p)

	def help(self,cmd_name):
		cmd=self.__get_cmd(cmd_name)
		self.__help(cmd)

	def __write(self,func,formatter,argv=None):
		if argv:
			func(formatter % argv)
		else:
			func(formatter)

	def write(self,formatter,*argv):
		self.__write(self.console.write,formatter,argv)

	def write_line(self,formatter,*argv):
		self.__write(self.console.write_line,formatter,argv)

	def warning(self,formatter,*argv):
		self.__write(self.console.yellow,formatter,argv)

	def info(self,formatter,*argv):
		self.__write(self.console.write_line,formatter,argv)

	def error(self,formatter,*argv):
		self.__write(self.console.red,formatter,argv)

	def success(self,formatter,*argv):
		self.__write(self.console.green,formatter,argv)

	def hightlight(self,formatter,*argv):
		self.__write(self.console.purple,formatter,argv)

	def get_props(self,p):
		result=[]
		for a in dir(p):
			if a.startswith('__'):
				continue
			result.append(a)
		return result

	def hint(self):
		if not self.client.container:
			self.write('$/>')
		elif not self.client.paths:
			self.write('$%s/>',self.client.container)
		else:
			self.write('$%s/%s/>',self.client.container,string.join(self.client.paths,'/'))

	def loop(self):
		while True:
			self.hint()
			input = raw_input()
			try:
				self.__call_cmd(input)
			except Exception,ex:
				self.warning(ex.message)

