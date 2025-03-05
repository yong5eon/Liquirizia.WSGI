# -*- coding: utf-8 -*-

from .Object import Object

from typing import List, Tuple, Any

__all__ = (
	'Value'
)


class Value(Object):
	"""Multi Part Form Data Value Object"""

	def __init__(self, name: str, value: Any = None):
		self.name = name
		self.value = value
		return

	def headers(self) -> List[Tuple[str, str]]:
		headers = []
		headers.append(('Content-Disposition', 'form-data; name="{}"'.format(self.name)))
		return headers

	def body(self) -> str:
		return str(self.value)
