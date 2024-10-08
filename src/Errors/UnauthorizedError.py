# -*- coding: utf-8 -*-

from ..Error import Error

__all__ = (
	'UnauthorizedError'
)


class UnauthorizedError(Error):
	"""
	Unauthorized Error Class, 401
	"""
	def __init__(self, reason, error=None):
		super(UnauthorizedError, self).__init__(reason, 401, 'Unauthorized', error)
		return
