# -*- coding: utf-8 -*-

from ..Error import Error

__all__ = (
	'GoneError'
)


class GoneError(Error):
	"""
	Gone Error Class, 410
	"""
	def __init__(self, reason, error=None):
		super(GoneError, self).__init__(reason, 410, 'Gone', error)
		return
