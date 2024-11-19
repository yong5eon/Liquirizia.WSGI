# -*- coding: utf-8 -*-

from .Request import Request
from .Response import Response

__all__ = (
	'ResponseWriter'
)


class ResponseWriter(object):
	"""Response Writer Class"""

	CRLF = '\r\n'

	def __init__(self, request: Request, sender: callable, cb: callable = None):
		self.request = request
		self.sender = sender
		self.writer = None
		self.cb = cb
		return
	
	def response(self, response: Response):
		if self.cb: response = self.cb(self.request, response)
		self.writer = self.sender(str(response), response.headers())
		if response.body:
			self.writer(response.body)
		self.writer(b'')
		return

	def send(self, status: int, message: str, headers: dict = None):
		response = Response(status, message, headers=headers)			
		if self.cb: response = self.cb(self.request, response)
		self.writer = self.sender(str(response), response.headers())
		return
	
	def write(self, buffer):
		self.writer(buffer)
		return
