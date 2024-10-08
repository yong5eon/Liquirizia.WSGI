# -*- coding: utf-8 -*-

from ..Error import Error

__all__ = (
	'ProxyAuthenticationRequiredError'
)


class ProxyAuthenticationRequiredError(Error):
	"""
	Proxy Authentication Required Error Class, 407
	"""
	def __init__(self, reason, error=None):
		super(ProxyAuthenticationRequiredError, self).__init__(reason, 407, 'Proxy Authentication Required', error)
		return
