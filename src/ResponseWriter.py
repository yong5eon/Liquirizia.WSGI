# -*- coding: utf-8 -*-

from .Response import Response

__all__ = (
	'ResponseWriter'
)


class ResponseWriter(object):
	"""Response Writer Class"""

	CRLF = '\r\n'

	def __init__(self, sender: callable, cb: callable = None):
		self.sender = sender
		self.writer = None
		self.cb = cb
		return
	
	def response(self, response: Response):
		if self.cb:
			response = self.cb(response)
		self.writer = self.sender(str(response), response.headers())
		if response.body:
			self.writer(response.body)
		return

	def send(self, status: int, message: str, headers: dict = None):
		response = Response(status, message, headers=headers)			
		if self.cb:
			response = self.cb(response)
		self.writer = self.sender(str(response), response.headers())
		return
	
	def write(self, buffer):
		self.writer(buffer)
		return
