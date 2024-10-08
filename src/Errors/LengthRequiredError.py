# -*- coding: utf-8 -*-

from ..Error import Error

__all__ = (
	'LengthRequiredError'
)


class LengthRequiredError(Error):
	"""
	Length Required Error Class, 411
	"""
	def __init__(self, reason, error=None):
		super(LengthRequiredError, self).__init__(reason, 411, 'Length Required', error)
		return
