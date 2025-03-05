# -*- coding: utf-8 -*-

from .Object import Object

from os.path import split
from mimetypes import guess_type
from base64 import b64encode
from typing import List, Tuple

__all__ = (
	'File'
)


class File(Object):
	"""Multi Part Form Data File Object"""

	def __init__(self, name, path, filename=None, base64: bool = False):
		self.name = name
		self.format, self.charset = guess_type(path)
		self.filename = filename if filename else split(path)[1]
		self.b64 = base64
		self.path = path
		self.f = None
		return

	def headers(self) -> List[Tuple[str, str]]:
		headers = []
		headers.append(('Content-Disposition', 'form-data; name="{}"; filename="{}"'.format(self.name, self.filename)))
		headers.append(('Content-Type', '{}{}'.format(self.format, '; charset={}'.format(self.charset) if self.charset else '')))
		if self.b64:
			headers.append(('Content-Transfer-Encoding', 'base64'))
		return headers

	def open(self):
		self.f = open(self.path, 'rb')
		return True if self.f else False

	def read(self, size=None):
		return self.f.read(size)

	def close(self):
		if self.f:
			self.f.close()
			self.f = None
		return

	def body(self) -> bytes:
		if self.open():
			if self.b64:
				return b64encode(self.read())
			return self.read()
