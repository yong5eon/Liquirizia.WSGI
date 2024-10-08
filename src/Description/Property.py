# -*- coding: utf-8 -*-

from enum import  Enum

from typing import Any
from typing import Optional, Sequence

__all__ = (
	'Type',
	'Property',
)

class Type(str, Enum):
	Boolean = 'boolean'
	Integer = 'integer'
	Number = 'number'
	String = 'string'
	Array = 'array'

class Property(object): pass
class Property(object):
	def __init__(
		self,
		name: str,
		description: str = None,
		type: Type = None,
		format: str = None,
		min: Any = None,
		max: Any = None,
		default: Any = None,
		ins: Optional[Sequence[Any]] = None,
		required: bool = True,
		deprecated: bool = False,
	):
		self.name = name
		self.description = description
		self.type = type
		self.format = format
		self.min = min
		self.max = max
		self.default = default
		self.ins = ins
		self.required = required
		self.deprecated = deprecated
		return
