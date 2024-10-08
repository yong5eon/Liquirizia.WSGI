# -*- coding: utf-8 -*-

from ..Error import Error

__all__ = (
	'NotExtendedError'
)


class NotExtendedError(Error):
	"""
	NotExtended Error Class, 510
	"""
	def __init__(self, reason, error=None):
		super(NotExtendedError, self).__init__(reason, 510, 'Not Extended', error)
		return
