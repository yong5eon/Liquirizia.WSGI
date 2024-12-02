# -*- coding: utf-8 -*-

from os import pipe

__all__ = (
	'BufferedStream',
)


class BufferedStream(object):
	def __init__(self):
		self.i, self.o = pipe()
		self.reader = open(self.i, 'rb', buffering=0)
		self.writer = open(self.o, 'wb', buffering=0)
		return

	def __del__(self):
		self.reader.close()
		self.writer.close()
		return

	def read(self, size: int = -1):
		return self.reader.read(size)
	
	def readline(self, size: int = -1):
		return self.reader.readline(size)

	def write(self, buffer: bytes):
		self.writer.write(buffer)	
		self.writer.flush()
		return
