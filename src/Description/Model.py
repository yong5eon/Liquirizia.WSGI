# -*- coding: utf-8 -*-

from collections.abc import Mapping

from enum import  Enum

from typing import Any, Iterator, KeysView, ItemsView, ValuesView
from typing import Optional, Union, Sequence

__all__ = (
	'Type',
	'Boolean',
	'Integer',
	'Number',
	'String',
	'Array',
	'Object',
	'ObjectProperties',
)


class Model(Mapping):
	def __init__(self, **kwargs):
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
		ins: Optional[Sequence[str]] = None,
		required: bool = True,
		deprecated: bool = False,

	):
		super().__init__(
			type=type,
			description=description,
			format=format,
			minimum=min,
			maximum=max,
			default=default,
			enum=ins,
			required=required,
			deprecated=deprecated,
		)
		return

class Boolean(Value):
	def __init__(
		self, 
		description: str = None,
		default: Any = None,
		required: bool = True,
		deprecated: bool = False,

	):
		super().__init__(
			type=Type.Boolean,
			description=description,
			default=default,
			required=required,
			deprecated=deprecated,
		)
		return

class Integer(Value):
	def __init__(
		self, 
		description: str = None,
		format: str = None,
		min: Any = None,
		max: Any = None,
		default: Any = None,
		ins: Optional[Sequence[str]] = None,
		required: bool = True,
		deprecated: bool = False,

	):
		super().__init__(
			type=Type.Integer,
			description=description,
			format=format,
			min=min,
			max=max,
			default=default,
			ins=ins,
			required=required,
			deprecated=deprecated,
		)
		return

class Number(Value):
	def __init__(
		self, 
		description: str = None,
		format: str = None,
		min: Any = None,
		max: Any = None,
		default: Any = None,
		ins: Optional[Sequence[str]] = None,
		required: bool = True,
		deprecated: bool = False,

	):
		super().__init__(
			type=Type.Number,
			description=description,
			format=format,
			min=min,
			max=max,
			default=default,
			ins=ins,
			required=required,
			deprecated=deprecated,
		)
		return

class String(Value):
	def __init__(
		self, 
		description: str = None,
		format: str = None,
		min: Any = None,
		max: Any = None,
		default: Any = None,
		ins: Optional[Sequence[str]] = None,
		required: bool = True,
		deprecated: bool = False,

	):
		super().__init__(
			type=Type.String,
			description=description,
			format=format,
			min=min,
			max=max,
			default=default,
			ins=ins,
			required=required,
			deprecated=deprecated,
		)
		return

class ObjectProperties(Model): pass
class Object(Model):
	def __init__(
		self,
		properties: ObjectProperties,
		description: Optional[str] = None,
		requires: Optional[Sequence[str]] = None,
		deprecated: bool = False,
	):
		super().__init__(
			type=Type.Object,
			properties=properties,
			description=description,
			required=requires,
			deprecated=deprecated,
		)
		return
	
class Array(Model):
	def __init__(
		self,
		format: Optional[Union[Value,Object]]= None,
		description: str = None,
		required: bool = True,
		deprecated: bool = False,
	):
		super().__init__(
			type=Type.Array,
			items=format,
			description=description,
			required=required,
			deprecated=deprecated,
		)
