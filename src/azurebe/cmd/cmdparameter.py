#!/usr/bin/python
# Filename: cmdparameter.py

import shlex
import string

class CmdParameter:
	counter=0
	def __init__(self,optional=True,explicit=False,default_value=None):
		self.value=default_value
		self.idx=CmdParameter.counter
		self.optional=optional
		self.explicit=explicit
		CmdParameter.counter+=1

class CmdParameterItem:
	def __init__(self,name,item):
		self.name=name
		self.item=item

class CmdParameters:
	def __init__(self,option_optional=True,option_explicit=False,option_default=None):
		CmdParameter.counter=0
		self.option=CmdParameter(option_optional,option_explicit,option_default)
		self.alphanum='abcdfeghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
		self.wordchars=self.alphanum+'-?/=\\'
		self.posix=True
		self.whitespace_split=False
		self.argvs=[]
		self.kwargvs={}

	def fields(self):
		fs =[CmdParameterItem(name,item) for name,item in self.__dict__.items() if isinstance(item,CmdParameter)]
		fs.sort(lambda v1, v2: cmp(v1.item.idx, v2.item.idx))
		return fs

	def __get_token(self,shlex):
		try:
			return shlex.next()
		except:
			return None

	def get_params(self,input):
		s= shlex.shlex(input,self.posix)
		s.wordchars = self.wordchars
		s.whitespace_split=self.whitespace_split
		argvs=[]
		kwargvs={}
		c=self.__get_token(s)
		while True:
			if not c:
				break
			n=self.__get_token(s)
			if not n:
				argvs.append(c)
				break
			if n==':':
				v=self.__get_token(s)
				if not v:
					raise Exception('arg [%s] value can not be empty.' % c)
				kwargvs[c]=v
				c=self.__get_token(s)
			else:
				argvs.append(c)
				c=n
		self.argvs=argvs
		self.kwargvs=kwargvs
		return (argvs,kwargvs)

	def generate(self,input):
		argv,kwargv = self.get_params(input)
		p=self
		fields = p.fields()
		result=[]
		idx=0
		op=fields[0]
		implicit_fields=[f for f in fields if not f.item.explicit]
		length=len(implicit_fields)
		for arg in argv:
			if arg.startswith('-'):
				op.item.value=arg.lstrip('-')
			else:
				idx+=1
				if idx == length:
					break
				implicit_fields[idx].item.value=arg

		for p in fields:
			if p.name in kwargv.keys():
				p.item.value=kwargv[p.name]