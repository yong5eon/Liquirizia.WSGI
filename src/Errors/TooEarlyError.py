# -*- coding: utf-8 -*-

from ..Error import Error

__all__ = (
	'TooEarlyError'
)


class TooEarlyError(Error):
	"""
	Too Early Error Class, 425
	"""
	def __init__(self, reason, error=None):
		super(TooEarlyError, self).__init__(reason, 425, 'Too Early', error)
		return
