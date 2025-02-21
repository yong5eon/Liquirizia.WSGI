# -*- coding: utf-8 -*-

from Liquirizia.Validator import Validator, Pattern
from Liquirizia.Validator.Patterns import (
	IsToNone,
	IsDataObject,
	IsDictionary,
	IsArray,
	IsString,
	IsFloat,
	IsInteger,
	IsBool,
)
from Liquirizia.Validator.Patterns.DataObject import (
	IsRequiredIn as IsRequiredInDataObject,
	IsMappingOf as IsMappingOfDataObject,
)
from Liquirizia.Validator.Patterns.Dictionary import (
	IsRequiredIn as IsRequiredInDictionary,
	IsMappingOf as IsMappingOfDictionary,
)

from ..Error import Error
from typing import Dict, Sequence, Union, Iterable

__all__ = (
	'Parameter',
	'Header',
	'QueryString',
	'Content',
	'Boolean',
	'Integer',
	'Number',
	'String',
	'Array',
	'Object',
)


class Parameter(Validator):
	"""Paramter Validator"""
	def __init__(
		self,
		mappings: Dict[str, Union[Pattern, Sequence[Pattern]]],
	):
		for k, patterns in mappings.items() if mappings else []:
			if not isinstance(patterns, (list, tuple)): patterns = [patterns]
			mappings[k] = Validator(*patterns)
		super().__init__(IsDataObject(IsMappingOfDataObject(mappings)))
		return


class Header(Validator):
	"""Header Validator"""
	def __init__(
		self,
		mappings: Dict[str, Union[Pattern, Sequence[Pattern]]] = None,
		requires: Union[str, Sequence[str]] = None,
		requiresError: Error = None,
	):
		for k, patterns in mappings.items() if mappings else []:
			if not isinstance(patterns, Sequence): patterns = [patterns]
			mappings[k] = Validator(*patterns)
		if requires and not isinstance(requires, Sequence):
			requires = [requires]
		super().__init__(IsDictionary(
			IsRequiredInDictionary(*requires if requires else [] , error=requiresError),
			IsMappingOfDictionary(mappings if mappings else {}),
		))
		return


class QueryString(Validator):
	"""QueryString Validator"""
	def __init__(
		self,
		mappings: Dict[str, Union[Pattern, Sequence[Pattern]]] = None,
		requires: Union[str, Sequence[str]] = None,
		requiresError: Error = None,
		required: bool = True,
		error: Error = None,
	):
		for k, patterns in mappings.items() if mappings else []:
			if not isinstance(patterns, Sequence): patterns = [patterns]
			mappings[k] = Validator(*patterns)
		if requires and not isinstance(requires, Sequence):
			requires = [requires]
		super().__init__(IsDataObject(
			IsRequiredInDataObject(*requires if requires else [] , error=requiresError),
			IsMappingOfDataObject(mappings if mappings else {}, error=error),
			error=error,
		) if required else IsToNone(IsDataObject(
			IsRequiredInDataObject(*requires if requires else [] , error=requiresError),
			IsMappingOfDataObject(mappings if mappings else {}, error=error),
			error=error,
		)))
		return


class Content(Validator):
	"""Content Validator"""
	def __init__(
		self,
		pattern: Pattern,
	):
		super().__init__(pattern)
		return


class Boolean(Content):
	"""Boolean Body Validator"""
	def __init__(
		self,
		*patterns: Iterable[Pattern],
		required: bool = True,
		error: Error = None,
	):
		super().__init__(IsBool(*patterns, error=error) if required else IsToNone(IsBool(*patterns, error=error)))
		return


class Integer(Content):
	"""Integer Body Validator"""
	def __init__(
		self,
		*patterns: Iterable[Pattern],
		required: bool = True,
		error: Error = None,
	):
		super().__init__(IsInteger(*patterns, error=error) if required else IsToNone(IsInteger(*patterns, error=error)))
		return


class Number(Content):
	"""Number Body Validator"""
	def __init__(
		self,
		*patterns: Iterable[Pattern],
		required: bool = True,
		error: Error = None,
	):
		super().__init__(IsFloat(*patterns, error=error) if required else IsToNone(IsFloat(*patterns, error=error)))
		return


class String(Content):
	"""String Body Validator"""
	def __init__(
		self,
		*patterns: Iterable[Pattern],
		required: bool = True,
		error: Error = None,
	):
		super().__init__(IsString(*patterns, error=error) if required else IsToNone(IsString(*patterns, error=error)))
		return


class Array(Content):
	"""Array Body Validator"""
	def __init__(
		self,
		*patterns: Iterable[Pattern],
		required: bool = True,
		error: Error = None,
	):
		super().__init__(IsArray(
			*patterns,
			error=error,
		) if required else IsToNone(IsArray(
			*patterns,
			error=error,
		)))
		return


class Object(Content):
	"""Parameters(Dictionary) Body Validator"""
	def __init__(
		self,
		mappings: Dict[str, Union[Pattern, Sequence[Pattern]]] = None,
		requires: Union[str, Sequence[str]] = None,
		requiresError: Error = None,
		required: bool = True,
		error: Error = None,
	):
		for k, patterns in mappings.items() if mappings else []:
			if not isinstance(patterns, (list, tuple)): patterns = [patterns]
			mappings[k] = Validator(*patterns)
		if requires and not isinstance(requires, Sequence):
			requires = [requires]
		super().__init__(IsDictionary(
			IsRequiredInDictionary(*requires if requires else [] , error=requiresError),
			IsMappingOfDictionary(mappings if mappings else {}, error=error),
			error=error,
		) if required else IsToNone(IsDataObject(
			IsRequiredInDictionary(*requires if requires else [] , error=requiresError),
			IsMappingOfDictionary(mappings if mappings else {}, error=error),
			error=error,
		)))
		return
