# -*- coding: utf-8 -*-

from .Request import Request
from .Response import Response

from .Handler import Handler
from .CORS import CORS

__all__ = (
	'ResponseWriter'
)


class ResponseWriter(object):
	"""Response Writer Class"""

	CRLF = '\r\n'

	def __init__(self, request: Request, sender: callable, handler: Handler = None, cors: CORS = None):
		self.request = request
		self.sender = sender
		self.writer = None
		self.handler = handler
		self.cors = cors
		return
	
	def response(self, response: Response):
		if self.handler: response = self.handler.onRequestResponse(self.request, response)
		if self.cors:
			for k, v in self.cors.toHeaders().items(): response.header(k, v)
		self.writer = self.sender(str(response), response.headers())
		if response.body:
			self.writer(response.body)
		self.writer(b'')
		return

	def send(self, status: int, message: str, headers: dict = None):
		response = Response(status, message, headers=headers)			
		if self.handler: response = self.handler.onRequestResponse(self.request, response)
		if self.cors:
			for k, v in self.cors.toHeaders().items(): response.header(k, v)
		self.writer = self.sender(str(response), response.headers())
		return
	
	def write(self, buffer):
		self.writer(buffer)
		return
