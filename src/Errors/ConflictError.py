# -*- coding: utf-8 -*-

from ..Error import Error

__all__ = (
	'ConflictError'
)


class ConflictError(Error):
	"""
	Conflict Error Class, 409
	"""
	def __init__(self, reason, error=None):
		super(ConflictError, self).__init__(reason, 409, 'Conflict', error)
		return
