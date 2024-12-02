# -*- coding: utf-8 -*-

from .BufferedStream import BufferedStream

from typing import List, Tuple

__all__ = (
	'Sender',
	'SenderStream',
)


class Sender(object):
	def __init__(self):
		self.status = None
		self.message = None
		self.headers = None
		self.buffer = bytearray()
		pass

	def __call__(self, status: str, headers: List[Tuple[str, str]] = None):
		self.status, self.message = status.split(' ', maxsplit=1)
		self.headers = headers
		return self.write

	def write(self, buffer: bytes):
		self.buffer += buffer
		return
	

class SenderStream(object):
	def __init__(self):
		self.status = None
		self.message = None
		self.headers = None
		self.buffer = BufferedStream()
		pass

	def __call__(self, status: str, headers: List[Tuple[str, str]] = None):
		self.status, self.message = status.split(' ', maxsplit=1)
		self.headers = headers
		return self.write

	def write(self, buffer: bytes):
		self.buffer.write(buffer)
		return
	
	def read(self, size: int = -1):
		return self.buffer.read(size)
	
	def readline(self, size: int = -1):
		return self.buffer.readline(size)
	
	def close(self):
		self.buffer.writer.close()
		return
	