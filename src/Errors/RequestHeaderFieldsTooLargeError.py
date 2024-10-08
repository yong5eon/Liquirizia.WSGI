# -*- coding: utf-8 -*-

from ..Error import Error

__all__ = (
	'RequestHeaderFieldsTooLargeError'
)


class RequestHeaderFieldsTooLargeError(Error):
	"""
	Request Header Fields Too Large Error Class, 431
	"""
	def __init__(self, reason, error=None):
		super(RequestHeaderFieldsTooLargeError, self).__init__(reason, 431, 'Request Header Fields Too Large', error)
		return
