#!/usr/bin/python
# FileName: blobclient.py

import string
import os
from storageclient import StorageClient

class BlobClient(StorageClient):

	def __init__(self):
		StorageClient.__init__(self)
		self.container=None
		self.containers=[]
		self.paths=[]
		self.path_separator='/'
		self.block_size=1024*1024*4

	def __check_service(self):
		StorageClient.check_service(self)

	def __check_container(self):
		if not self.container:
			raise Exception('The container can not be empty')

	def __get_block_prefix(self,prefix):
		p= string.join(self.paths,self.path_separator)
		if p:
			p += self.path_separator
		if prefix:
			p += prefix
		if not p:
			p=None
		return p

	def set_container(self,container):
		self.__check_service()
		if not container:
			self.container=None
			return
		if not container in self.containers:
			self.list_containers()

		if not container in self.containers:
			raise Exception('The container [%s] does not exists'%container)
		
		self.container = container		

	def append_path(self,path):
		self.paths.append(path)

	def pop_path(self):
		if self.paths:
			self.paths.pop()

	def list_containers(self,prefix=None,marker=None,maxresults=None,include=None):
		self.__check_service()
		if not prefix:
			prefix=None
		list = self.service.list_containers(prefix,marker,maxresults,include)
		self.containers=[c.name for c in list]
		return list

	def list_blobs(self,prefix=None, recursion=False, marker=None,maxresults=None,include=None):
		self.__check_service()
		self.__check_container()
		p= self.__get_block_prefix(prefix)
		#todo: check the recursion value and do job
		list=self.service.list_blobs(self.container,p,marker,maxresults,include)
		return list

	def list_blobs_for_container(self,container_name,prefix=None):
		self.__check_service()
		if prefix:
			return self.service.list_blobs(container_name)
		else:
			return self.service.list_blobs(container_name,prefix)

	def create_container(self,container_name,metadata,access):
		self.__check_service()
		if not container_name:
			raise Exception('The container name can not be empty.')

		self.service.create_container(container_name.lower(),metadata,access)

	def delete_container(self,container_name):
		self.__check_service()
		self.service.delete_container(container_name)
		if self.container==name:
			self.container=None
			self.paths=[]


	def get_blob(self,blob_name,file_path):
		self.__check_service()
		self.__check_container()
		blob_name = self.__get_block_prefix(blob_name)
		if not blob_name:
			raise Exception('the blob name can not be empty')

		props = self.service.get_blob_properties(self.container, blob_name)
		blob_size=int(props['content-length'])
		index = 0
		if not os.path.exists(os.path.dirname(file_path)):
			os.makedirs(os.path.dirname(file_path))
		with open(file_path, 'wb') as f:
			while index < blob_size:
				chunk_range = 'bytes={}-{}'.format(index, index + self.block_size - 1)
				data = self.service.get_blob(self.container, blob_name, x_ms_range=chunk_range)
				length = len(data)
				index += length
				if length > 0:
					f.write(data)
					if length < self.block_size:
						break
				else:
					break

	def put_blob(self,blob_name,file_path):
		self.__check_service()
		self.__check_container()
		self.service.put_blob(self.container, blob_name, '', 'BlockBlob')
		blob_name=self.__get_block_prefix(blob_name)
		
		file_size=size = os.path.getsize(file_path)
		if file_size>self.block_size:
			block_ids = []
			index = 0
			with open(file_path, 'rb') as f:
				while True:
					data = f.read(self.block_size)
					if data:
						length = len(data)
						block_id = base64.b64encode(str(index))
						blob_service.put_block(self.container, blob_name, data, block_id)
						block_ids.append(block_id)
						index += 1
					else:
						break

			self.service.put_block_list(self.container, blob_name, block_ids)

		else:
			with open(file_path, 'rb') as f:
				data=f.read()
				self.service.put_blob(self.container,blob_name,data,'BlockBlob')


		
