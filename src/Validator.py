# -*- coding: utf-8 -*-

from Liquirizia.Validator import Validator, Pattern
from .Validators import (
	IsObject,
)
from .Description import (
	Value,
	Schema,
)
from .Decoder import Decoder
from .Request import Request
from .Error import Error
from .Errors import (
	UnauthorizedError,
	ForbiddenError,
	BadRequestError,
	UnsupportedMediaTypeError,
)
from .Headers import (
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
	'Content',
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
		error: Error = None,
		schema: Dict[str, Value] = None,
	):
		self.va = Validator(IsObject(
			mappings=parameters,
			error=error if error else BadRequestError('Invalid parameters'),
		))
		self.schema = schema
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
		error: Error = None,
		schema: Dict[str, Value] = None,
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
		self.va = Validator(IsObject(
			mappings=qs,
			requires=requires,
			requiresError=requiresError,
			error=error if error else BadRequestError('Invalid query string'),
		))
		self.schema = schema
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
		error: Error = None,
		schema: Dict[str, Value] = None,
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
			mappings=headers,
			requires=requires,
			requiresError=requiresError,
			error=error if error else BadRequestError('Invalid headers'),
		))
		self.schema = schema
		return
	def __call__(self, request: Request):
		headers = {}
		for k, v in request.headers():
			headers[k] = v
		headers = self.va(headers)
		for k, v in headers.items():
			request.header(k, v)
		return


class Content(object):
	"""Content Validator"""
	def __init__(
		self,
		decode: Decoder,
		va: Pattern,
		format: str = None,
		schema: Union[Value, Schema] = None,
	):
		self.decode = decode
		self.va = Validator(va)
		self.format = format
		self.schema = schema
		return
	def __call__(self, content: bytes):
		decoded = self.decode(content)
		return self.va(decoded)


class Body(object):
	"""Body Validator"""
	def __init__(
		self,
		content: Union[Content, Sequence[Content]],
		error: Error = None,
	):
		self.content = content
		if not isinstance(content, (list, tuple)):
			self.content = [content]
		self.error = error
		return
	def __call__(self, request: Request, content: bytes):
		type: ContentType = request.header('Content-Type')
		content = None
		for content in self.content:
			if type.format == content.format:
				content = content
				break
		if not content:
			if self.error:
				raise self.error
			raise UnsupportedMediaTypeError('Unsupported Media Type {}'.format(type.format))
		return content(content)
