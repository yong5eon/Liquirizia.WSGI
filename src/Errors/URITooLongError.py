# -*- coding: utf-8 -*-

from ..Error import Error

__all__ = (
	'URITooLongError'
)


class URITooLongError(Error):
	"""
	URI Too Long Error Class, 414
	"""
	def __init__(self, reason, error=None):
		super(URITooLongError, self).__init__(reason, 414, 'URI Too Long', error)
		return
