# -*- coding: utf-8 -*-

from .Request import Request

from io import BufferedReader, BytesIO, SEEK_END

__all__ = (
	'RequestReader'
)


class RequestReader(object):
	"""Request Reader Class"""

	CRLF = '\r\n'

	def __init__(self, reader: BytesIO):
		self.reader = BufferedReader(reader)
		self.cursor = 0
		return

	def read(self, size=None):
		self.reader.seek(self.cursor)
		buf = self.reader.read(size)
		self.cursor += len(buf)
		return buf
	
	def readline(self):
		self.reader.seek(self.cursor)
		line = self.reader.readline()
		if not line:
			return None
		self.cursor += len(line)
		return line

