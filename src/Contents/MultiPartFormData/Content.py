# -*- coding: utf-8 -*-

from ...Content import Content as BaseContent

from .Properties import Object

from uuid import uuid4
from typing import List, Tuple

__all__ = (
	'Content',
)


class Content(BaseContent):
	def __init__(self, charset='utf-8', boundary=None):
		self.charset = charset
		self.boundary = boundary if boundary else uuid4().hex
		self.parts = []
		return

	def add(self, part: Object) -> 'Content':
		self.parts.append(part)
		return self

	def headers(self) -> List[Tuple[str, str]]:
		headers = []
		headers.append(('Content-Type', 'multipart/form-data; boundary={}'.format(self.boundary)))
		return headers

	def body(self) -> bytes:
		CRLF = '\r\n'
		buffer = bytes()
		for part in self.parts:
			buffer += '--{}{}'.format(self.boundary, CRLF).encode(self.charset)
			for key, value in part.headers():
				buffer += '{}: {}'.format(key, value, CRLF).encode(self.charset)
				buffer += '{}'.format(CRLF).encode(self.charset)
			buffer += '{}'.format(CRLF).encode(self)
			buf = part.body()
			buffer += buf if isinstance(buf, bytes) else buf.encode(self.charset)
			buffer += '{}'.format(CRLF).encode(self.charset)
		buffer += '--{}--'.format(self.boundary, CRLF).encode(self.charset)
		buffer += '{}'.format(CRLF).encode(self.charset)
		return buffer
