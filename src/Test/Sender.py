# -*- coding: utf-8 -*-

from typing import List, Tuple

__all__ = (
	'TestRequest',
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
