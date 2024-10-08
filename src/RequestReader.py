# -*- coding: utf-8 -*-

from .Request import Request

from io import BufferedReader

__all__ = (
	'RequestReader'
)


class RequestReader(object):
	"""Request Reader Class"""

	CRLF = '\r\n'

	def __init__(self, reader):
		self.reader = reader
		return

	def read(self, size=None):
		return self.reader.read(size)

	def chunk(self):
		line = self.reader.readline()
		size = int(line, 16)
		if not size:
			return None
		buffer = self.reader.read(size)
		self.reader.readline()
		return buffer
