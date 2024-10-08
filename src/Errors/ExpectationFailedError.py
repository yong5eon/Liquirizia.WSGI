# -*- coding: utf-8 -*-

from ..Error import Error

__all__ = (
	'ExpectationFailedError'
)


class ExpectationFailedError(Error):
	"""
	Expectation Failed Error Class, 417
	"""
	def __init__(self, reason, error=None):
		super(ExpectationFailedError, self).__init__(reason, 417, 'Expectation Failed', error)
		return
