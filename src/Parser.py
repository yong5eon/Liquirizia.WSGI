# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from urllib.parse import parse_qs, unquote_plus
from json import loads
from ast import literal_eval

from typing import Dict, Any

__all__ = (
	'Parser',
	'FormUrlParser',
	'FormUrlEncodedParser',
	'JavaScriptObjectNotataionParser',
)


class Decoder(metaclass=ABCMeta):
	"""Content Decoder Interface"""
	@abstractmethod
	def __call__(self, body: str) -> Dict[str, Any]:
		raise NotImplemented('{} must be implemented __call__'.format(self.__class__.__name__))
	@abstractmethod
	def format(self):
		raise NotImplemented('{} must be implemented format'.format(self.__class__.__name__))
	@abstractmethod
	def charset(self):
		raise NotImplemented('{} must be implemented charset'.format(self.__class__.__name__))


class FormUrlEncodedDecoder(Decoder):
	def __init__(self, charset='utf-8'):
		self.__charset__ = charset
		return
	def __call__(self, body: str) -> Dict[str, Any]:
		qs = parse_qs(body, keep_blank_values=True)
		q = {}
		for (key, value) in qs.items():
			if len(value) == 0:
				q[key] = None
				continue
			elif len(value) == 1:
				try:
					q[key] = unquote_plus(literal_eval(value[0]))
				except:
					q[key] = unquote_plus(value[0]) if len(value[0]) else None
				continue
			else:
				q[key] = unquote_plus(value)
		return q
	def format(self): return 'application/x-www-form-urlencoded'
	def charset(self): return self.__charset__


class JavaScriptObjectNotationDecoder(Decoder):
	def __call__(self, body: str) -> Dict[str, Any]:
		return loads(body)

