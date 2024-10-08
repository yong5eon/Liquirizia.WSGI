# -*- coding: utf-8 -*-

from ..Error import Error

__all__ = (
	'UnprocessableEntityError'
)


class UnprocessableEntityError(Error):
	"""
	Unprocessable Entity Error Class, 422
	"""
	def __init__(self, reason, error=None):
		super(UnprocessableEntityError, self).__init__(reason, 422, 'Unprocessable Entity', error)
		return
