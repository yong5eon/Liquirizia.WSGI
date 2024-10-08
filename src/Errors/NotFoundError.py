# -*- coding: utf-8 -*-

from ..Error import Error

__all__ = (
	'NotFoundError'
)


class NotFoundError(Error):
	"""
	Not Found Error Class, 404
	"""
	def __init__(self, reason, error=None):
		super(NotFoundError, self).__init__(reason, 404, 'Not Found', error)
		return
