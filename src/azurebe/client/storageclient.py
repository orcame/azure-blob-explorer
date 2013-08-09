# !/usr/bin/python
# FileName: storageclient.py

from azure.storage import BlobService
class StorageClient():

	def __init__(self):
		self.account_info=None
		self.service=None

	def check_service(self):
		if not self.service:
			raise Exception('The service can not be empty.')

	def connect_stroage(self,account_name,account_key,protocol="http",host_base=".blob.core.windows.net"):
		self.account_info=AccountInfo(None,account_name,account_key,protocol,host_base)
		self.service=BlobService(account_name,account_key,protocol,host_base)

class AccountInfo:
	def __init__(self,id=None,account_name=None,account_key=None,protocol='http',host_base='.blob.core.windows.net'):
		self.id=id
		self.account_name=account_name
		self.account_key=account_key
		self.protocol=protocol
		self.host_base=host_base

