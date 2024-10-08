# -*- coding: utf-8 -*-

from ..Error import Error

__all__ = (
	'NotAcceptableError'
)


class NotAcceptableError(Error):
	"""
	Not Acceptable Error Class, 406
	"""
	def __init__(self, reason, error=None):
		super(NotAcceptableError, self).__init__(reason, 406, 'Not Acceptable', error)
		return
