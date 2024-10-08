# -*- coding: utf-8 -*-

from ..Error import Error

__all__ = (
	'PreconditionRequiredError'
)


class PreconditionRequiredError(Error):
	"""
	Precondition Required Error Class, 428
	"""
	def __init__(self, reason, error=None):
		super(PreconditionRequiredError, self).__init__(reason, 428, 'Precondition Required', error)
		return
