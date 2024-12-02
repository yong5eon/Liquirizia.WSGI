# -*- coding: utf-8 -*-

from ..RequestReader import RequestReader

from time import sleep

from typing import Optional

__all__ = (
	'ChunkedStreamReader'
)

class ChunkedStreamReader(object):
	def __init__(self, reader: RequestReader):
		self.reader= reader
		self.format = None
		self.charset = None
		return
	
	def chunk(self) -> Optional[bytes]:
		while True:
			line = self.reader.readline()
			if not line:
				sleep(0)
				continue
			size = int(line, 16)
			if not size:
				return None
			buffer = self.reader.read(size)
			line = self.reader.readline()
			return buffer
