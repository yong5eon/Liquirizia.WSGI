# -*- coding: utf-8 -*-

from Liquirizia.Serializer import Serializer

from urllib.parse import parse_qs
from ast import literal_eval

__all__ = (
	'Decoder'
)


class Decoder(Serializer):
	"""Decoder Class for JSON"""

	def __call__(self, obj):
		if not isinstance(obj, str):
			raise RuntimeError('{} is not string'.format(obj))
		qs = parse_qs(obj, keep_blank_values=True)
		q = {}
		for (key, value) in qs.items():
			if len(value) == 0:
				q[key] = None
				continue
			elif len(value) == 1:
				try:
					q[key] = literal_eval(value[0])
				except:
					q[key] = value[0] if len(value[0]) else None
				continue
			else:
				q[key] = value
		return q
