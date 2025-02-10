# -*- coding: utf-8 -*-

from traceback import format_tb

from typing import Dict, Any

__all__ = (
	'Error',
)


class Error(BaseException):
	"""Error Class of WSGI"""
	def __init__(
		self,
		reason: str,
		status: int,
		message: str,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		error: BaseException = None
	):
		super(Error, self).__init__(reason)
		self.status = status
		self.message = message
		self.headers = headers
		self.body = body
		self.format = format
		self.charset = charset
		self.error = error
		return

	@property 
	def traceback(self):
		reason = '{}\n'.format(str(self.error) if self.error else str(self))
		if self.error:
			reason += ''.join(format_tb(self.error.__traceback__)).strip().replace(' ' * 4, ' ' * 2)
		else:
			reason += ''.join(format_tb(self.__traceback__)).strip().replace(' ' * 4, ' ' * 2)
		return reason
	
	@property
	def __traceback__(self):
		if self.error:
			return self.error.__traceback__
		return super(Error, self).__traceback__
