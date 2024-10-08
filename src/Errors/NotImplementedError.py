# -*- coding: utf-8 -*-

from ..Error import Error

__all__ = (
	'NotImplementedError'
)


class NotImplementedError(Error):
	"""
	Not Implemented Error Class, 501
	"""
	def __init__(self, reason, error=None):
		super(NotImplementedError, self).__init__(reason, 501, 'Not Implemented', error)
		return
