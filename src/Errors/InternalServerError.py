# -*- coding: utf-8 -*-

from ..Error import Error

__all__ = (
	'InternalServerError'
)


class InternalServerError(Error):
	"""
	Internal Server Error Class, 500
	"""
	def __init__(self, reason, error=None):
		super(InternalServerError, self).__init__(reason, 500, 'Internal Server Error', error)
		return
