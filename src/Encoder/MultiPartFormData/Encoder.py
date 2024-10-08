# -*- coding: utf-8 -*-

from Liquirizia.System.Util import GenerateUUID

from ..Encoder import Encoder as EncoderBase
from .Properties import Object

__all__ = (
	'Encoder'
)


class Encoder(EncoderBase):
	def __init__(self, charset='utf-8', boundary=GenerateUUID()):
		self.charset = charset
		self.boundary = boundary
		self.parts = []
		return

	def add(self, part: Object):
		self.parts.append(part)
		return

	def headers(self):
		headers = []
		headers.append(('Content-Type', 'multipart/form-data; boundary={}'.format(self.boundary)))
		headers.append(('Content-Length', len(self.encode())))
		return headers

	def encode(self):
		CRLF = '\r\n'
		buffer = bytes()
		for part in self.parts:
			buffer += '--{}{}'.format(self.boundary, CRLF).encode()
			for key, value in part.headers():
				buffer += '{}: {}'.format(key, value, CRLF).encode()
				buffer += '{}'.format(CRLF).encode()
			buffer += '{}'.format(CRLF).encode()
			buffer += part.body()
			buffer += '{}'.format(CRLF).encode()
		buffer += '--{}--'.format(self.boundary, CRLF).encode()
		buffer += '{}'.format(CRLF).encode()
		return buffer

