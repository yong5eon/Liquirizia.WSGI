# -*- coding: utf-8 -*-

from collections.abc import Mapping

from enum import  Enum

from typing import Any, Iterator, KeysView, ItemsView, ValuesView
from typing import Optional, Sequence, Dict, Union

__all__ = (
	'Model',
	'Type',
	'Value',
	'Schema',
)


class Model(Mapping):
	def __init__(self, **kwargs: Dict[str, Union['Value', 'Schema']]):
		self.__properties__ = kwargs
		return

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


class Type(str, Enum):
	Boolean = 'boolean'
	Integer = 'integer'
	Number = 'number'
	String = 'string'
	Array = 'array'
	Object = 'object'


class Value(Model):
	def __init__(
		self, 
		type: Type,
		description: str = None,
		format: str = None,
		min: Any = None,
		max: Any = None,
		default: Any = None,
		enum: Optional[Sequence[str]] = None,
		required: bool = True,
		deprecated: bool = False,

	):
		super().__init__(
			type=type,
		)
		if description: self['description'] = description
		if format: self['format'] = format
		if min: self['minimum'] = min
		if max: self['maximum'] = max
		if default: self['default'] = default
		if enum: self['enum'] = enum
		if required: self['required'] = required
		if deprecated: self['deprecated'] = deprecated
		return


class Schema(object):
	def __init__(
		self,
		name: str,
		format: Value,
	):
		self.name = name
		self.format = format
		return

