# -*- coding: utf-8 -*-

from .Object import Object

__all__ = (
	'Value'
)


class Value(Object):
	"""Multi Part Form Data Value Object"""

	def __init__(self, name, value=None):
		self.name = name
		self.value = value
		return

	def headers(self):
		headers = []
		headers.append(('Content-Disposition', 'form-data; name="{}"'.format(self.name)))
		return headers

	def body(self):
		return self.value.encode()
