# -*- coding: utf-8 -*-

from ..Error import Error

__all__ = (
	'ServiceUnavailableError'
)


class ServiceUnavailableError(Error):
	"""
	Service Unavailable Error Class, 503
	"""
	def __init__(self, reason, error=None):
		super(ServiceUnavailableError, self).__init__(reason, 503, 'Service Unavailable', error)
		return
