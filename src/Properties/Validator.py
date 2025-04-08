# -*- coding: utf-8 -*-

from Liquirizia.Validator import Validator, Pattern
from Liquirizia.Validator.Patterns import IsDataObject, IsObject
from Liquirizia.Validator.Patterns.DataObject import (
	IsRequiredIn as IsRequiredInDataObject,
	IsMappingOf as IsMappingOfDataObject,
)
from Liquirizia.Validator.Patterns.Object import (
	IsRequiredIn as IsRequiredInObject,
	IsMappingOf as IsMappingOfObject,
)
from Liquirizia.Description import (
	Value,
	Schema,
)
from ..Decoder import Decoder
from ..Request import Request
from ..Error import Error
from ..Errors import (
	UnauthorizedError,
	ForbiddenError,
	BadRequestError,
	UnsupportedMediaTypeError,
)
from ..Headers import (
	Authorization as AuthorizationHeader,
	Cookie,
	ContentType,
)

from abc import ABCMeta, abstractmethod
from typing import Dict, Sequence, Union, Any

__all__ = (
	'Origin',
	'Auth',
	'Authorization',
	'HTTP',
	'Cookie',
	'Parameter',
	'QueryString',
	'Header',
	'Body',
)


class Origin(object):
	def __init__(
		self,
		origin: Union[str, Sequence[str]] = None,
		all: bool = False,
		error: Error = None,
	):
		self.matches = origin
		if not isinstance(self.matches, (list, tuple)):
			self.matches = [self.matches]
		self.all = all 
		self.error = error
		return
	def __call__(self, request: Request):
		origin = request.header('Origin')
		match = None
		for m in self.matches:
			if origin == m:
				match = m
				break
		if match or self.all:
			return
		if self.error:
			raise self.error
		raise ForbiddenError('Origin {} is not allowed'.format(origin))


class Auth(metaclass=ABCMeta):
	@abstractmethod
	def __call__(self, request: Request):
		raise NotImplementedError('{} must be implemented __call__'.format(
			self.__class__.__name__,
		))


class Authorization(metaclass=ABCMeta):
	@abstractmethod
	def __call__(self, value: Any) -> Any:
		raise NotImplementedError('{} must be implemented __call__'.format(
			self.__class__.__name__,
		))


class HTTP(Auth):
	def __init__(
		self,
		scheme: str,
		auth: Authorization,
		format: str = None,
		schemeError: Error = None,
		schemeParameters: Dict[str, Any] = None,
		error: Error = None,
	):
		self.scheme = scheme
		self.authorization = auth
		self.format = format
		self.schemeError = schemeError
		self.schemeParameters = schemeParameters
		self.error = error
		return
	def __call__(self, request: Request):
		authorization: AuthorizationHeader = request.header('Authorization')
		if not authorization:
			if self.error:
				raise self.error
			raise UnauthorizedError('Authorization not found')
		if not authorization.scheme == self.scheme:
			if self.schemeError:
				raise self.schemeError
			raise UnauthorizedError(
				'Authorization scheme not supported',
				headers={
					'WWW-Authenticate': '{} {}'.format(
						self.scheme,
						','.join([
							'{}="{}"'.format(k, v) for k, v in self.schemeParameters.items()
						]) if self.schemeParameters else '',
					),
				},
			)
		request.session = self.authorization(authorization.credentials)
		return


class Cookie(Auth):
	def __init__(
		self,
		auth: Authorization,
		error: Error = None,
	):
		self.authorization = auth
		self.error = error
		return
	def __call__(self, request: Request) -> Any:
		cookies = request.header('Cookie')
		if not cookies:
			if self.error:
				raise self.error
			raise UnauthorizedError('Cookie not found')
		request.session = self.authorization(cookies)
		return


class Parameter(object):
	"""Paramter Validator"""
	def __init__(
		self,
		parameters : Dict[str, Union[Pattern, Sequence[Pattern]]],
		format: Dict[str, Union[Value, Schema]] = None,
	):
		self.va = Validator(IsDataObject(IsMappingOfDataObject(parameters)))
		self.format = format
		return
	def __call__(self, request: Request):
		request.params = self.va(request.params)
		return


class QueryString(object):
	"""QueryString Validator"""
	def __init__(
		self,
		qs: Dict[str, Union[Pattern, Sequence[Pattern]]],
		requires: Union[str, Sequence[str]] = None,
		requiresError: Error = None,
		format: Dict[str, Union[Value, Schema]] = None,
	):
		if not requiresError:
			if requires:
				if not isinstance(requires, (list, tuple)):
					requires = [requires]
				requiresError = BadRequestError('Missing required query string {}'.format(
					','.join(requires),
				))
			else:
				requiresError = BadRequestError('Missing required query string')
		self.va = Validator(IsDataObject(
			IsRequiredInDataObject(*requires if requires else [], error=requiresError),
			IsMappingOfDataObject(qs),
		))
		self.format = format
		return
	def __call__(self, request: Request):
		request.args = self.va(request.args)
		return


class Header(object):
	"""Header Validator"""
	def __init__(
		self,
		headers: Dict[str, Union[Pattern, Sequence[Pattern]]],
		requires: Union[str, Sequence[str]] = None,
		requiresError: Error = None,
		format: Dict[str, Union[Value, Schema]] = None,
	):
		if not requiresError:
			if requires:
				if not isinstance(requires, (list, tuple)):
					requires = [requires]
				requiresError = BadRequestError('Missing required headers {}'.format(
					','.join(requires),
				))
			else:
				requiresError = BadRequestError('Missing required headers')
		self.va = Validator(IsObject(
			IsRequiredInObject(*requires if requires else [], error=requiresError),
			IsMappingOfObject(headers),
		))
		self.format = format 
		return
	def __call__(self, request: Request):
		headers = {}
		for k, v in request.headers():
			headers[k] = v
		headers = self.va(headers)
		for k, v in headers.items():
			request.header(k, v)
		return


class Body(object):
	"""Body Validator"""
	def __init__(
		self,
		content: Pattern,
		decoders: Dict[str, Decoder],
		error: Error = None,
		unsupportedError: Error = None,
		format: Union[Value, Schema] = None,
		required: bool = True,
	):
		self.va = Validator(content)
		self.decoders = decoders
		self.error = error
		self.unsupportedError = unsupportedError
		self.format = format
		self.required = required
		return
	def __call__(self, request: Request, content: bytes):
		type: ContentType = request.header('Content-Type')
		if not type:
			if self.error:
				raise self.error
			raise BadRequestError('Content-Type not found')
		if type.format not in self.decoders.keys():
			if self.unsupportedError:
				raise self.unsupportedError
			raise UnsupportedMediaTypeError('Unsupported Media Type {}'.format(type.format))
		content = self.decoders[type.format](content)
		return self.va(content)
