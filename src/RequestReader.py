# -*- coding: utf-8 -*-

from .Request import Request

from io import BufferedReader, BytesIO, SEEK_END

__all__ = (
	'RequestReader'
)


class RequestReader(object):
	"""Request Reader Class"""

	CRLF = '\r\n'

	def __init__(self, reader: BufferedReader):
		self.reader = reader
		return

	def read(self, size: int = -1):
		return self.reader.read(size)
	
	def readline(self, size: int = -1):
		return self.reader.readline(size)

