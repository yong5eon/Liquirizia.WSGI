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

	def begin(self, headers: dict = {}):
		headers['Content-Type'] = 'text/event-stream'
		headers['Cache-Control'] = 'no-cache'
		self.writer.send(200, 'OK', headers=headers)
		return

	def emit(self, data: str, event: str = None, id: str = None):
		# text/event-stream is always encoded in utf-8
		CRLF = '\r\n'
		if id:
			self.writer.write('id: {}{}'.format(id, CRLF).encode('utf-8'))
		if event:
			self.writer.write('event: event{}'.format(id, CRLF).encode('utf-8'))
		for line in data.split('\n'):
			if not line: continue
			self.writer.write('data: {}{}'.format(line, CRLF).encode('utf-8'))
		self.writer.write(CRLF.encode('utf-8'))
		return
	
	def retry(self, ms: int):
		CRLF = '\r\n'
		self.writer.write('retry: {}{}'.format(ms, CRLF).encode('utf-8'))
		self.writer.write(CRLF.encode('utf-8'))

	def end(self):
		self.writer.write(b'')
		return
