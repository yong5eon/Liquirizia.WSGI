# -*- coding: utf-8 -*-

from Liquirizia.Serializer import Serializer

from urllib.parse import urlencode

__all__ = (
	'Encoder'
)


class Encoder(Serializer):
	"""Encoder for JSON"""

	def __call__(self, obj):
		if not isinstance(obj, dict):
			raise RuntimeError('{} is not dict'.format(obj))
		return urlencode(obj, doseq=True)
