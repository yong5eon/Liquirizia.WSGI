# -*- coding: utf-8 -*-

from ..Error import Error

__all__ = (
	'NetworkAuthenticationRequiredError'
)


class NetworkAuthenticationRequiredError(Error):
	"""
	Network Authentication Required Error Class, 511
	"""
	def __init__(self, reason, error=None):
		super(NetworkAuthenticationRequiredError, self).__init__(reason, 511, 'Network Authentication Required', error)
		return
