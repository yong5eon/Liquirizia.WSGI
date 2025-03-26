# -*- coding: utf-8 -*-

from .Value import Model, Type, Value, Schema
from typing import Optional, Union, Sequence, Any, Dict

__all__ = (
	'Boolean',
	'Integer',
	'Number',
	'String',
	'Array',
	'Object',
	'ObjectProperties',
)


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
		enum: Optional[Sequence[str]] = None,
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
			enum=enum,
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
		enum: Optional[Sequence[str]] = None,
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
			enum=enum,
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
		enum: Optional[Sequence[str]] = None,
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
			enum=enum,
			required=required,
			deprecated=deprecated,
		)
		return


class ObjectProperties(Model):
	def __init__(self, **kwargs: Dict[str, Union[Value, Schema]]):
		for k, v in kwargs.items():
			kwargs[k] = {'$ref': '#/components/schemas/{}'.format(v.name)} if isinstance(v, Schema) else v
		super().__init__(**kwargs)
		return 
class Object(Model):
	def __init__(
		self,
		properties: ObjectProperties = ObjectProperties(),
		description: Optional[str] = None,
		requires: Optional[Sequence[str]] = None,
		deprecated: bool = False,
	):
		super().__init__(
			type=Type.Object,
			properties=properties,
		)
		if description: self['description'] = description
		if requires: self['required'] = requires
		if deprecated: self['deprecated'] = deprecated
		return


class Array(Model):
	def __init__(
		self,
		format: Optional[Union[Value, Object, 'Array', Schema]] = None,
		description: str = None,
		required: bool = True,
		deprecated: bool = False,
	):
		super().__init__(
			type=Type.Array,
		)
		if format: self['items'] = {'$ref': '#/components/schemas/{}'.format(format.name)} if isinstance(format, Schema) else format
		if description: self['description'] = description
		if required: self['required'] = required
		if deprecated: self['deprecated'] = deprecated
		return
