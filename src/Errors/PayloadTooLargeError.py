# -*- coding: utf-8 -*-

from ..Error import Error

__all__ = (
	'PayloadTooLargeError'
)


class PayloadTooLargeError(Error):
	"""
	Payload Too Large Error Class, 413
	"""
	def __init__(self, reason, error=None):
		super(PayloadTooLargeError, self).__init__(reason, 413, 'Payload Too Large', error)
		return
