# -*- coding: utf-8 -*-

from ..Error import Error

__all__ = (
	'VersionNotSupportedError'
)


class VersionNotSupportedError(Error):
	"""
	HTTP Version Not Supported Error Class, 505
	"""
	def __init__(self, reason, error=None):
		super(VersionNotSupportedError, self).__init__(reason, 505, 'Version Not Supported', error)
		return
