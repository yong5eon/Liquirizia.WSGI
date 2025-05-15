# -*- coding: utf-8 -*-

from typing import Dict, Any

__all__ = (
	'Error',
)


class Error(BaseException):
	"""Error Class of WSGI"""
	def __init__(
		self,
		status: int,
		message: str,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		reason: str = None,
		error: BaseException = None,
		extra: Any = None,
	):
		super(Error, self).__init__()
		self.status = status
		self.message = message
		self.headers = headers
		self.body = body
		self.format = format
		self.charset = charset
		self.reason = reason
		self.error = error
		self.extra = extra
		return
	
	def __repr__(self):
		if self.reason:
			return '{}: {}'.format(self.__class__.__name__, self.reason)
		return self.__class__.__name__
	
	def __str__(self):
		if self.reason:
			return '{}: {}'.format(self.__class__.__name__, self.reason)
		return self.__class__.__name__

	@property
	def __traceback__(self):
		if self.error:
			return self.error.__traceback__
		return super(Error, self).__traceback__
