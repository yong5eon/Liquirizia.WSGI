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

from collections.abc import Sequence, Mapping
from re import match, split
from typing import Type, Dict, Any, Iterator, KeysView, ItemsView, ValuesView

__all__ = (
	'Header',
	'HeaderWithParameters',
	'HeaderAsParameter',
	'HeaderAsParameters',
	'HeaderAsList',
)


class Header(object):
	"""Header Class"""
	def __init__(self, value: str):
		self.__val__ = value
		return
	# def __str__(self): return self.__val__.strip().replace('"','').replace('<','').replace('>','')
	def __str__(self): return self.__val__.strip()


class HeaderWithParameters(Header):
	def __init__(self, value: str, sep: str = ';', paramsep: str = ','):
		super().__init__(value)
		self.__value__, self.__parameters__ = self.parse(value, sep=sep, paramsep=paramsep)
		return
	def parse(self, value: str, sep: str, paramsep: str):
		ts = value.strip().split(sep, maxsplit=1)
		val = ts[0].strip().replace('"','').replace('<','').replace('>','')
		params = {}
		if len(ts) > 1:
			for p in ts[1].strip().split(paramsep):
				ps = p.strip().split('=')
				params[ps[0].strip().replace('"','').replace('<','').replace('>','')] = ps[1].strip().replace('"','').replace('<','').replace('>','') if len(ps) > 1 else None
		return val, params
	@property
	def value(self): return self.__value__
	@property
	def parameters(self): return self.__parameters__


class HeaderAsParameter(Header):
	def __init__(self, value):
		super().__init__(value)
		ps = value.strip().split('=')
		self.__key__ = ps[0].strip().replace('"','').replace('<','').replace('>','')
		self.__weight__ = ps[1].strip().replace('"','').replace('<','').replace('>','') if len(ps) > 1 else None
		return
	@property
	def key(self): return self.__key__
	@property
	def weight(self): return self.__weight__

class HeaderAsParameters(Header, Mapping):
	def __init__(self, value: str, sep: str = ','):
		super().__init__(value)
		self.__properties__ = self.parse(value, sep)
		return
	def parse(self, value: str, sep: str):
		params = {}
		for p in value.split(sep):
			ps = p.strip().split('=')
			k = ps[0].strip().replace('"','').replace('<','').replace('>','')
			v = ps[1].strip().replace('"','').replace('<','').replace('>','') if len(ps) > 1 else None
			params[k] = v
		return params
	# implements of Mapping
	def __getitem__(self, key: Any) -> Any:
		return self.__properties__.__getitem__(key)
	def __setitem__(self, key: Any, value: Any) -> None:
		return self.__properties__.__setitem__(key, value)
	def __delitem__(self, key: Any) -> None:
		return self.__properties__.__delitem__(key)
	def __iter__(self) -> Iterator:
		return self.__properties__.__iter__()
	def __len__(self) -> int:
		return self.__properties__.__len__()
	def __contains__(self, key: object) -> bool:
		return self.__properties__.__contains__(key)
	def keys(self) -> KeysView:
		return self.__properties__.keys()
	def items(self) -> ItemsView:
		return self.__properties__.items()
	def values(self) -> ValuesView:
		return self.__properties__.values()
	def __eq__(self, other: object) -> bool:
		return self.__properties__.__eq__(other)
	def __ne__(self, value: object) -> bool:
		return self.__properties__.__ne__(value)
	def get(self, key: object) -> Any:
		return self.__properties__.get(key)


class HeaderAsList(Header, Sequence):
	"""List Type Header Class"""
	def __init__(self, value: str, sep: str = ',', format: Type[Header] = Header, options: Dict[str, Any]={}):
		super().__init__(value)
		self.__properties__ = []
		for token in value.split(sep=sep):
			if token.strip(): self.__properties__.append(format(token.strip(), **options))
		return
	# implements of Sequence
	def __contains__(self, value):
		return self.__properties__.__contains__(value)
	def __len__(self):
		return self.__properties__.__len__()
	def __iter__(self):
		return self.__properties__.__iter__()
	def __reversed__(self):
		return self.__properties__.__reversed__()
	def __getitem__(self, index):
		return self.__properties__.__getitem__(index)
	def index(self, value: any, start: int = 0, stop: int = ...) -> int:
		return self.__properties__.index(value, start, stop)
	def count(self, value: any) -> int:
		return self.__properties__.count(value)
