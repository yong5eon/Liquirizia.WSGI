# -*- coding: utf-8 -*-

from ..ResponseWriter import ResponseWriter
from ..Response import Response

__all__ = (
	'ServerSentEvents'
)

class ServerSentEvents(object):
	def __init__(self, writer: ResponseWriter):
		self.writer = writer
		self.charset = None
		return
	
	def response(self, response: Response):
		return self.writer.response(response)

	def begin(self, headers: dict = {}, charset: str = None):
		self.charset = charset
		headers['Content-Type'] = 'text/event-stream{}'.format(
			'; charset={}'.format(charset) if charset else ''
		)
		# TODO: fix header problems
		# according to PEP333, chunkend and keep-alive is commented
		#
		# headers['Connection'] = 'keep-alive'
		headers['Cache-Control'] = 'no-cache'
		self.writer.send(200, 'OK', headers=headers)
		return

	def emit(self, data: str):
		CRLF = '\r\n'
		self.writer.write('data: {}'.format(data).encode(self.charset if self.charset else ''))
		self.writer.write(CRLF.encode(self.charset if self.charset else ''))
		self.writer.write(CRLF.encode(self.charset if self.charset else ''))
		return

	def end(self):
		self.writer.write(b'')
		return
