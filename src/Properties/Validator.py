# -*- coding: utf-8 -*-

from Liquirizia.Validator import Validator, Pattern
from Liquirizia.Validator.Patterns import (
	IsToNone,
	IsDictionary,
	IsRequiredIn,
	IsMappingOf,
)

from ..Error import Error
from typing import Dict, Sequence, Union

__all__ = (
	'Parameter',
	'Header',
	'QueryString',
	'Body',
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
		super().__init__(IsDictionary(IsMappingOf(mappings)))
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
			IsRequiredIn(*requires if requires else [] , error=requiresError),
			IsMappingOf(mappings if mappings else {}),
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
		super().__init__(IsDictionary(
			IsRequiredIn(*requires if requires else [] , error=requiresError),
			IsMappingOf(mappings if mappings else {}, error=error),
			error=error,
		) if required else IsToNone(IsDictionary(
			IsRequiredIn(*requires if requires else [] , error=requiresError),
			IsMappingOf(mappings if mappings else {}, error=error),
			error=error,
		)))
		return


class Body(Validator):
	"""Body Validator"""
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
			IsRequiredIn(*requires if requires else [] , error=requiresError),
			IsMappingOf(mappings if mappings else {}, error=error),
			error=error,
		) if required else IsToNone(IsDictionary(
			IsRequiredIn(*requires if requires else [] , error=requiresError),
			IsMappingOf(mappings if mappings else {}, error=error),
			error=error,
		)))
		return
