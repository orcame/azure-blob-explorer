#!/usr/bin/python
# Filename: copy.py
'''
copy the file(s) from remote to local or from local to remote

	copy from to 
	copy * d:/ --copy all file under current path from remote to local d disk.

	you must do this under a container path.
'''
import string
import os
from cmdparameter import (CmdParameter,CmdParameters)

class _Params(CmdParameters):
	def __init__(self):
		CmdParameters.__init__(self)
		self.f=CmdParameter()
		self.t=CmdParameter()
		self.wordchars=self.alphanum+'-:?/=\\'
		self.whitespace_split=True

def download_files(client,prefix,local_folder):
	if not os.path.exists(local_folder):
		os.makedirs(local_folder)

	blobs = client.list_blobs(prefix)
	if not local_folder.endswith('/'):
		local_folder+='/'
	path_idx=len(string.join(client.paths,'/'))
	if path_idx>0:
		path_idx+=1

	for blob in blobs:
		name = blob.name[path_idx:]
		print '\t','download blob',name,'...'
		file_name=local_folder+name
		client.get_blob(name,file_name)

def upload_files(client,local_path):
	l=len(local_path)
	for root, dirs, files in os.walk(local_path, True):
		for name in files:
			local_name=os.path.join(root,name)
			print '\t','upload',local_name,'...'
			blob_name=local_name[l:].replace('\\','/')
			client.put_blob(blob_name,local_name)

def is_local_path(path):
	if not path:
		return False
	return os.path.isabs(path)

def do_action(cmd,p):
	f = p.f.value
	t = p.t.value
	if is_local_path(f) and is_local_path(t):
		raise Exception('can not copy from local to local.')
	if is_local_path(f):
		upload_files(cmd.client,f)
	else:
		if f=='*':
			f=None
		download_files(cmd.client,f,t)
	
