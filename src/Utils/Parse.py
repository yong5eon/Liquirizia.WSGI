# -*- coding: utf-8 -*-
#
# https://www.iana.org/assignments/http-fields/http-fields.xhtml
# https://developer.mozilla.org/ko/docs/Web/HTTP/Headers 
#
# HTTP Types
# - Request Header
# - Response Header
# - Representation)Entity) Headers
# - Payload Headers
#
# Header Structures 
# - String
# - Structured
#   - List
#   - Dict
#   - Item
#   - Token

from datetime import datetime
from abc import ABC, abstractmethod
from typing import Dict, Tuple, List, Any, Optional

__all__ = (
	'Parse',
	'ParseBoolean',
	'ParseString',
	'ParseStringWithParameters',
	'ParseInteger',
	'ParseFloat',
	'ParseParameter',
	'ParseParameters',
	'ParseList',
	'ParseDate',
)

class Parse(ABC):
	"""Parser Abstract Class"""
	@abstractmethod
	def __call__(self, value: str):
		raise NotImplementedError('{} must be implemented __call__'.format(self.__class__.__name__))
	def strip(self, value: str):
		value = value.strip()
		if len(value):
			if value[0] == '"': value = value[1:]
			if value[-1:] == '"': value = value[:-1]
		return value


class ParseBoolean(Parse):
	def __init__(self, true: str = '1', false: str = None):
		self.true = true
		self.false = false
		return
	def __call__(self, value: str) -> Optional[bool]:
		if self.true == value: return True
		if self.false and self.false == value: return False
		return


class ParseString(Parse):
	"""String Parser Class"""
	def __call__(self, value: str) -> str:
		return self.strip(value)
	

class ParseStringWithParameters(Parse):
	"""String Parser Class included Parameters"""
	def __init__(self, sep: str = ';', paramsep: str = ','):
		self.sep = sep
		self.paramsep = paramsep
		return
	def __call__(self, value: str) -> Tuple[str, Dict[str, str]]:
		ts = value.strip().split(self.sep, maxsplit=1)
		val = self.strip(ts[0])
		params = {}
		if len(ts) > 1:
			for p in ts[1].strip().split(self.paramsep):
				ps = p.strip().split('=')
				params[self.strip(ps[0])] = self.strip(ps[1]) if len(ps) > 1 else None
		return val, params


class ParseInteger(Parse):
	"""Integer Parser Class"""
	def __call__(self, value: str) -> str:
		return int(eval(self.strip(value)))


class ParseFloat(Parse):
	"""Float Parser Class"""
	def __call__(self, value: str) -> str:
		return float(eval(self.strip(value)))
	

class ParseDate(Parse):
	"""Float Parser Class"""
	def __call__(self, value: str) -> str:
		return datetime.strptime(self.strip(value), '%a, %d %b %Y %H:%M:%S GMT')
	

class ParseParameter(Parse):
	"""Parameter Parser Class"""
	def __init__(self, sep: str = '='):
		self.sep = sep
		return
	def __call__(self, value: str) -> Tuple[str, str]:
		ps = value.split(self.sep, 1)
		k = self.strip(ps[0])
		v = self.strip(ps[1]) if len(ps) > 1 else None
		return k, v


class ParseParameters(Parse):
	"""Parameters Parser Class"""
	def __init__(self, sep: str = ',', paramsep: str = '='):
		self.sep = sep
		self.paramsep = paramsep
		return
	def __call__(self, value: str) -> Dict[str, str]:
		params = {}
		for p in value.split(self.sep):
			if not self.strip(p): continue
			ps = self.strip(p).split(self.paramsep, 1)
			k = self.strip(ps[0])
			v = self.strip(ps[1]) if len(ps) > 1 else None
			params[k] = v
		return params


class ParseList(Parse):
	"""List Parser Class"""
	def __init__(self, sep: str = ',', fetch: Parse = ParseString()):
		self.sep = sep
		self.fetch = fetch
		return
	def __call__(self, value: str) -> List[Any]:
		_ = []
		for token in value.split(sep=self.sep):
			_.append(self.fetch(self.strip(token)))
		return _

