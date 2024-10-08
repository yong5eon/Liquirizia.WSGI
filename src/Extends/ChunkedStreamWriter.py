# -*- coding: utf-8 -*-

from ..ResponseWriter import ResponseWriter
from ..Response import Response

__all__ = (
	'StreamChunked'
)

class ChunkedStreamWriter(object):
	def __init__(self, writer: ResponseWriter):
		self.writer = writer
		self.format = None
		self.charset = None
		return
	
	def response(self, response: Response):
		return self.writer.response(response)

	def begin(self, headers: dict = {}, format: str = None, charset: str = None):
		self.format = format
		self.charset = charset
		if format:
			headers['Content-Type'] = '{}{}'.format(
				format,
				'; charset={}'.format(charset) if charset else ''
			)
		# TODO: fix header problems
		# according to PEP333, chunkend and keep-alive is commented
		#
		# headers['Transfer-Encoding'] = 'chunked'
		# headers['Connection'] = 'keep-alive'
		headers['Cache-Control'] = 'no-cache'
		self.writer.send(200, 'OK', headers=headers)
		return

	def chunk(self, buffer):
		CRLF = '\r\n'
		size = '{:x}'.format(len(buffer) if buffer else 0)
		self.writer.write(size.encode())
		self.writer.write(CRLF.encode())
		self.writer.write(buffer)
		self.writer.write(CRLF.encode())
		return
	
	def end(self):
		CRLF = '\r\n'
		size = '{:x}'.format(0)
		self.writer.write(size.encode())
		self.writer.write(CRLF.encode())
		return
