# -*- coding: utf-8 -*-

from ..Util import ToHeaderName

from Liquirizia.Serializer import SerializerHelper

from io import BytesIO

from typing import Dict

__all__ = (
	'TestResponse',
)


class TestResponse(object):
	def __init__(
		self,
		status: int,
		message: str,
		headers: Dict[str, str] = None,
		body: bytes = None,
	):
		from cgi import parse_header
		self.status = status
		self.message = message
		self.headers = {}
		for k, v in headers.items() if headers else []:
			args, kwargs = parse_header(v)
			self.headers[ToHeaderName(k)] = {
				'expr': str(v),
				'args': args.split(','),
				'kwargs': kwargs
			}
		if self.header('Transfer-Encoding') == 'chunked':
			buffer = bytes()
			buf = BytesIO(body)
			while True:
				line = buf.readline()
				size = int(line, 16)
				if not size:
					break
				buffer += buf.read(size)
				line = buf.readline()
			self.body = SerializerHelper.Decode(
				buffer,
				self.format,
				self.charset
			) if buffer else None
		else:
			self.body = SerializerHelper.Decode(
				body,
				self.format,
				self.charset
			) if body else None
		return

	def header(self, key: str):
		if key not in self.headers:
			return None
		return self.headers[key]['expr']
	
	@property
	def size(self):
		if 'Content-Length' not in self.headers.keys():
			return 0
		return int(self.headers['Content-Length']['expr'])

	@property
	def format(self):
		if 'Content-Type' not in self.headers.keys():
			return None
		return self.headers['Content-Type']['args'][0]

	@property
	def charset(self):
		if 'Content-Type' not in self.headers.keys():
			return None
		if 'charset' not in self.headers['Content-Type']['kwargs'].keys():
			return None
		return self.headers['Content-Type']['kwargs']['charset']
