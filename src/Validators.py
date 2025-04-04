# -*- coding: utf-8 -*-

from Liquirizia.Validator import Validator, Pattern

from .Error import Error
from .Errors import BadRequestError
from typing import Union, Iterable, Type, Sequence, Dict, Mapping
from abc import abstractmethod

__all__ = (
	'IsBoolean',
	'ToBoolean',
	'IsInteger',
	'ToInteger',
	'IsNumber',
	'ToNumber',
	'IsString',
	'ToString',
	'IsArray',
	'ToArray',
	'IsObject',
	'ToObject',
)


class Evaluate(Pattern):
	@abstractmethod
	def __call__(self, parameter):
		raise NotImplementedError('{} must be implemented __call__'.format(self.__class__.__name__))


class IsTypeOf(Pattern):
	def __init__(
		self, 
		type: Type,
		eval: Evaluate = None,
		patterns: Sequence[Pattern] = (),
		error: Error = None,
		required: bool = True,
		requiredError: Error = None,
	):
		self.type = type
		self.eval = eval
		self.patterns = patterns if isinstance(patterns, Iterable) else (patterns,)
		self.required = required
		self.error = error
		self.requiredError = requiredError
		return

	def __call__(self, parameter):
		if parameter is None:
			if self.required:
				if self.requiredError:
					raise self.requiredError
				raise BadRequestError('value is None')
			return parameter
		if self.eval:
			try:
				parameter = self.eval(parameter)
			except Exception as e:
				if self.error:
					raise self.error
				raise BadRequestError('Invalid value {}'.format(parameter))
		if not isinstance(parameter, self.type):
			if self.error:
				raise self.error
			raise BadRequestError('{} must be {}'.format(
				'\'{}\''.format(parameter) if isinstance(parameter, str) else parameter, 
				self.type.__name__,
			))
		for pattern in self.patterns:
			parameter = pattern(parameter)
		return parameter

	def __repr__(self):
		if issubclass(self.__class__, IsTypeOf):	
			return '{}({})'.format(
				self.__class__.__name__,
				', '.join([p.__repr__() for p in self.patterns]) if self.patterns and len(self.patterns) else ''
			)
		return '{}({}{})'.format(
			self.__class__.__name__,
			self.type.__name__,
			', ({})'.format(
				', '.join([p.__repr__() for p in self.patterns])
			) if self.patterns and len(self.patterns) else ''
		)


class IsBoolean(IsTypeOf):
	def __init__(
		self,
		*patterns: Iterable[Pattern],
		required: bool = True,
		error: Error = None,
		requiredError: Error = None,
	):
		return super().__init__(
			bool,
			patterns,
			required=required,
			error=error,
			requiredError=requiredError,
		)


class ToBoolean(IsTypeOf):
	def __init__(
		self,
		*patterns: Iterable[Pattern],
		required: bool = True,
		error: Error = None,
		requiredError: Error = None,
	):
		return super().__init__(
			bool,
			patterns,
			eval=bool,
			required=required,
			error=error,
			returnedError=requiredError,
		)


class IsInteger(IsTypeOf):
	def __init__(
		self,
		*patterns: Iterable[Pattern],
		required: bool = True,
		error: Error = None,
		requiredError: Error = None,
	):
		return super().__init__(
			int,
			patterns,
			required=required,
			error=error,
			returnedError=requiredError,
		)


class ToInteger(IsTypeOf):
	def __init__(
		self,
		*patterns: Iterable[Pattern],
		required: bool = True,
		error: Error = None,
		requiredError: Error = None,
	):
		return super().__init__(
			int,
			patterns,
			eval=int,
			required=required,
			error=error,
			returnedError=requiredError,
		)


class IsNumber(IsTypeOf):
	def __init__(
		self,
		*patterns: Iterable[Pattern],
		required: bool = True,
		error: Error = None,
		requiredError: Error = None,
	):
		return super().__init__(
			float,
			patterns,
			required=required,
			error=error,
			requiredError=requiredError,
		)


class ToNumber(IsTypeOf):
	def __init__(
		self,
		*patterns: Iterable[Pattern],
		required: bool = True,
		error: Error = None,
		requiredError: Error = None,
	):
		return super().__init__(
			float,
			patterns,
			eval=float,
			required=required,
			error=error,
			returnedError=requiredError,
		)


class IsString(IsTypeOf):
	def __init__(
		self,
		*patterns: Iterable[Pattern],
		required: bool = True,
		error: Error = None,
		requiredError: Error = None,
	):
		return super().__init__(
			str,
			patterns,
			required=required,
			error=error,
			requiredError=requiredError,
		)


class ToString(IsTypeOf):
	def __init__(
		self,
		*patterns: Iterable[Pattern],
		required: bool = True,
		error: Error = None,
		requiredError: Error = None,
	):
		return super().__init__(
			str,
			patterns,
			eval=str,
			required=required,
			error=error,
			returnedError=requiredError,
		)


class IsIterable(Pattern):
	def __init__(
		self,
		eval: Evaluate = None,
		patterns: Iterable[Pattern] = (),
		min: int = None,
		max: int = None,
		size: int = None,
		required: bool = True,
		error: Error = None,
		minError: Error = None,
		maxError: Error = None,
		sizeError: Error = None,
		requiredError: Error = None,
	):
		self.patterns = patterns if isinstance(patterns, Iterable) else (patterns,)
		self.eval = eval
		self.error = error
		self.required = required
		self.requiredError = requiredError
		self.min = min
		self.minError = minError
		self.max = max
		self.maxError = maxError
		self.size = size
		self.sizeError = sizeError
		return
	def __repr__(self):
		return '{}({})'.format(
			self.__class__.__name__,
			', '.join([p.__repr__() for p in self.patterns])
		)
	def __call__(self, parameter):
		if parameter is None:
			if self.required:
				if self.requiredError: raise self.requiredError
				if self.error: raise self.error
				raise BadRequestError('value is None')
			return parameter
		if self.eval:
			try:
				parameter = self.eval(parameter)
			except Exception as e:
				if self.error: raise self.error
				raise BadRequestError('Invalid value {}'.format(parameter))
		if not isinstance(parameter, Iterable):
			if self.error: raise self.error
			raise BadRequestError('{} must be iterable'.format(parameter))
		if self.min and len(parameter) < self.min:
			if self.minError: raise self.minError
			if self.error: raise self.error
			raise BadRequestError('{} must be greater than {}'.format(parameter, self.min))
		if self.max and len(parameter) > self.max:
			if self.maxError: raise self.maxError
			if self.error: raise self.error
			raise BadRequestError('{} must be less than {}'.format(parameter, self.max))
		if self.size and len(parameter) != self.size:
			if self.sizeError: raise self.sizeError
			if self.error: raise self.error
			raise BadRequestError('{} must be {}'.format(parameter, self.size))
		for pattern in self.patterns:
			for i, e in enumerate(parameter):
				parameter[i] = pattern(e)
		return parameter


class IsArray(IsIterable):
	def __init__(
		self,
		*patterns: Iterable[Pattern],
		min: int = None,
		max: int = None,
		size: int = None,
		required: bool = True,
		error: Error = None,
		minError: Error = None,
		maxError: Error = None,
		sizeError: Error = None,
		requiredError: Error = None,
	):
		return super().__init__(
			patterns=patterns,
			min=min,
			max=max,
			size=size,
			required=required,
			error=error,
			minError=minError,
			maxError=maxError,
			sizeError=sizeError,
			requiredError=requiredError
		)


class ToArray(IsIterable):
	def __init__(
		self,
		*patterns: Iterable[Pattern],
		eval: Evaluate = list,
		min: int = None,
		max: int = None,
		size: int = None,
		required: bool = True,
		error: Error = None,
		minError: Error = None,
		maxError: Error = None,
		sizeError: Error = None,
		requiredError: Error = None,
	):
		return super().__init__(
			eval=eval,
			patterns=patterns,
			min=min,
			max=max,
			size=size,
			required=required,
			error=error,
			minError=minError,
			maxError=maxError,
			sizeError=sizeError,
			requiredError=requiredError
		)


class IsMapping(Pattern):
	def __init__(
		self,
		eval: Evaluate = None,
		mappings: Dict[str, Union[Validator, Pattern, Sequence[Pattern]]] = {},
		requires: Union[str, Sequence[str]] = None,
		required: bool = True,
		error: Error = None,
		requiresError: Error = None,
		requiredError: Error = None,
	):
		self.eval = eval
		self.mappings = self.__mapper__(mappings)
		self.requires = requires if isinstance(requires, Iterable) else (requires,)
		self.required = required
		self.error = error
		self.requiredError = requiredError
		self.requiresError = requiresError
		return

	def __mapper__(self, mappings: Dict[str, Validator]) -> Dict[str, Validator]:
		if not isinstance(mappings, dict):
			raise TypeError('{} must be dict'.format(mappings))
		for key, value in mappings.items():
			if isinstance(value, Sequence):
				mappings[key] = Validator(*value)
				continue
			if isinstance(value, Pattern):
				mappings[key] = Validator(value)
				continue
			if isinstance(value, Validator):
				mappings[key] = value
				continue
			raise ValueError('Invalid mapping table, {} must be dictionary or listable of Patterns, or callable based Pattern'.format(value))
		return mappings

	def __repr__(self) -> str:
		return '{}({})'.format(
			self.__class__.__name__,
			', '.join(
				['{}: {}'.format(k, repr(v)) for k, v in self.mappings.items()]
			)
		)
	
	def __call__(self, parameter):
		if parameter is None:
			if self.required:
				if self.requiredError: raise self.requiredError
				if self.error: raise self.error
				raise BadRequestError('value is None')
			return parameter
		if self.eval:
			try:
				parameter = self.eval(parameter)
			except Exception as e:
				if self.error: raise self.error
				raise BadRequestError('Invalid value {}'.format(parameter))
		if not isinstance(parameter, Mapping):
			if self.error: raise self.error
			raise BadRequestError('{} must be dict'.format(parameter))
		keys = parameter.keys()
		for arg in self.requires:
			if arg not in keys:
				if self.requiresError: raise self.requiresError
				if self.error: raise self.error
				raise BadRequestError('{} is required in {}'.format(arg, parameter))
		if self.mappings:
			for key, validator in self.mappings.items():
				parameter[key] = validator(parameter[key] if key in parameter.keys() else None)
		return parameter


class IsObject(IsMapping):
	def __init__(
		self,
		mappings: Dict[str, Union[Validator, Pattern, Sequence[Pattern]]] = {},
		requires: Union[str, Sequence[str]] = None,
		required: bool = True,
		error: Error = None,
		requiresError: Error = None,
		requiredError: Error = None,
	):
		return super().__init__(
			mappings=mappings,
			requires=requires,
			required=required,
			error=error,
			requiredError=requiredError,
			requiresError=requiresError
		)


class ToObject(IsMapping):
	def __init__(
		self,
		mappings: Dict[str, Union[Validator, Pattern, Sequence[Pattern]]] = {},
		eval: Evaluate = dict,
		requires: Union[str, Sequence[str]] = None,
		required: bool = True,
		error: Error = None,
		requiresError: Error = None,
		requiredError: Error = None,
	):
		return super().__init__(
			eval=eval,
			mappings=mappings,
			requires=requires,
			required=required,
			error=error,
			requiredError=requiredError,
			requiresError=requiresError
		)
