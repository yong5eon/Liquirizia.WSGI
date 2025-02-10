# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from urllib.parse import parse_qs
from json import loads
from ast import literal_eval

from typing import Dict, Any

__all__ = (
	'Parser',
	'FormUrlEncodedParser',
	'JavaScriptObjectNotataionParser',
)


class Parser(metaclass=ABCMeta):
	"""Body Parser Interface"""
	@abstractmethod
	def __call__(self, body: str) -> Dict[str, Any]:
		raise NotImplemented('{} must be implemented __call__'.format(self.__class__.__name__))


class FormUrlEncodedParser(Parser):
	def __call__(self, body: str) -> Dict[str, Any]:
		qs = parse_qs(body, keep_blank_values=True)
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


class JavaScriptObjectNotationParser(Parser):
	def __call__(self, body: str) -> Dict[str, Any]:
		return loads(body)

