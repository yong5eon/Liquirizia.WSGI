# -*- coding: utf-8 -*-

from .Validators import (
	Authorization,
	Auth,
)

from ..Request import Request
from ..Error import Error
from ..Errors import  UnauthorizedError
from ..Headers import (
	Authorization as AuthorizationObject,
	Cookie as CookieObject,
)

from typing import Dict, List, Any
from enum import Enum

__all__ = (
	'Query',
	'Cookie',
	'Header',
	'HTTP',
	'OAuth2Implicit',
	'OAuth2Password',
	'OAuth2ClientCredentials',
	'OAuth2AuthorizationCode',
)


class Query(Auth):
	def __init__(
		self,
		name: str,
		auth: Authorization,
		optional: bool = False,
		requiredError: Error = None,
	):
		super().__init__(auth, optional)
		self.name = name
		self.requiredError = requiredError
		return
	def __call__(self, request: Request) -> Any:
		if not hasattr(request.qs, self.name):
			if self.optional: return
			if self.requiredError: raise self.requiredError
			raise UnauthorizedError(reason='Query {} is not found'.format(self.name))
		request.session = self.auth(getattr(request.qs, self.name))
		return


class Cookie(Auth):
	def __init__(
		self,
		name: str,
		auth: Authorization,
		optional: bool = False,
		requiredError: Error = None,
	):
		super().__init__(auth, optional)
		self.name = name
		self.requiredError = requiredError
		return
	def __call__(self, request: Request) -> Any:
		cookies: List[CookieObject] = request.header('Cookie')
		if not cookies:
			if self.optional: return
			if self.requiredError: raise self.requiredError
			raise UnauthorizedError(reason='Cookie is not found')
		_ = None
		for cookie in cookies:
			if cookie.name == self.name:
				_ = cookie
				break
		if not _:
			if self.optional: return
			if self.requiredError: raise self.requiredError
			raise UnauthorizedError(reason='Cookie {} is not found'.format(self.name))
		request.session = self.auth(_)
		return


class Header(Auth):
	def __init__(
		self,
		name: str,
		auth: Authorization,
		optional: bool = False,
		requiredError: Error = None,
	):
		super().__init__(auth, optional)
		self.name = name
		self.requiredError = requiredError
		return
	def __call__(self, request: Request) -> Any:
		_ = request.header(self.name)
		if not _:
			if self.optional: return
			if self.requiredError: raise self.requiredError
			raise UnauthorizedError(reason='Header {} is not found'.format(self.name))
		request.session = self.auth(_)
		return


class HTTP(Auth):
	def __init__(
		self,
		scheme: str,
		auth: Authorization,
		format: str = None,
		optional: bool = False,
		requiredError: Error = None,
		requiredErrorParameters: Dict[str, str] = None,
		schemeError: Error = None,
		schemeErrorParameters: Dict[str, str] = None,
	):
		super().__init__(auth, optional)
		self.scheme = scheme
		self.format = format
		self.requiredError = requiredError
		self.requiredErrorParameters = requiredErrorParameters
		self.schemeError = schemeError
		self.schemeErrorParameters = schemeErrorParameters
		return
	def __call__(self, request: Request):
		authorization: AuthorizationObject = request.header('Authorization')
		if not authorization:
			if self.optional: return
			if self.requiredError: raise self.requiredError
			headers = None
			if self.requiredErrorParameters:
				headers = {
					'WWW-Authorization': '{} {}'.format(
						self.scheme,
						', '.join([
							'{}="{}"'.format(k, v) for k, v in self.requiredErrorParameters.items()
						]),
					),
				}
			raise UnauthorizedError(
				headers=headers,
				reason='Authorization not found',
			)
		if authorization.scheme != self.scheme:
			if self.schemeError: raise self.schemeError
			headers = None
			if self.schemeErrorParameters:
				headers = {
					'WWW-Authorization': '{} {}'.format(
						self.scheme,
						', '.join([
							'{}="{}"'.format(k, v) for k, v in self.schemeErrorParameters.items()
						]),
					),
				}
			raise UnauthorizedError(
				headers=headers,
				reason='Authorization scheme not supported',
			)
		request.session = self.auth(authorization.credentials)
		return


class OAuth2Type(str, Enum):
	Password = 'password'
	Implicit = 'implicit'
	ClientCredentials = 'clientCredentials'
	AuthorizationCode = 'authorizationCode'
	def __str__(self): return self.value


class OAuth2(Auth):
	def __init__(
		self,
		type: OAuth2Type,
		scheme: str,
		auth: Authorization,
		optional: bool = False,
		requiredError: Error = None,
		schemeError: Error = None,
		authorizationUrl: str = None,
		tokenUrl: str = None,
		refreshUrl: str = None,
		scope: Dict[str, str] = None,
	):
		super().__init__(auth, optional)
		self.type = type
		self.scheme = scheme
		self.requiredError = requiredError
		self.schemeError = schemeError
		self.kwargs = {}
		if authorizationUrl: self.kwargs['authorizationUrl'] = authorizationUrl
		if tokenUrl: self.kwargs['tokenUrl'] = tokenUrl
		if refreshUrl: self.kwargs['refreshUrl'] = refreshUrl
		if scope: self.kwargs['scope'] = scope
		return

	def __call__(self, request: Request) -> Any:
		authorization: AuthorizationObject = request.header('Authorization')
		if not authorization:
			if self.optional: return
			if self.requiredError: raise self.requiredError
			kwargs = {
				'error': 'invalid_request',
				'error_description': 'Authorization not found',
			}
			kwargs.update(self.kwargs)
			raise UnauthorizedError(
				headers={
					'WWW-Authorization': '{} {}'.format(
						self.scheme,
						', '.join([
							'{}="{}"'.format(k, v) for k, v in kwargs.items()
						]),
					),
				},
				reason='Authorization not found',
			)
		if authorization.scheme != self.scheme:
			if self.optional: return
			if self.schemeError: raise self.schemeError
			kwargs = {
				'error': 'invalid_scheme',
				'error_description': 'Authorization scheme not supported',
			}
			kwargs.update(self.kwargs)
			headers = {
				'WWW-Authorization': '{} {}'.format(
					self.scheme,
					', '.join([
						'{}="{}"'.format(k, v) for k, v in kwargs.items()
					]),
				),
			}
			raise UnauthorizedError(
				headers=headers,
				reason='Authorization scheme not supported',
			)
		request.session = self.auth(authorization.credentials)
		return


class OAuth2Implicit(OAuth2):
	def __init__(
		self,
		scheme: str,
		auth: Authorization,
		optional: bool = False,
		requiredError: Error = None,
		schemeError: Error = None,
		authorizationUrl: str = None,
	):
		super().__init__(
			type=OAuth2Type.Implicit,
			scheme=scheme,
			auth=auth,
			optional=optional,
			requiredError=requiredError,
			schemeError=schemeError,
			authorizationUrl=authorizationUrl,
		)
		return


class OAuth2Password(OAuth2):
	def __init__(
		self,
		scheme: str,
		auth: Authorization,
		optional: bool = False,
		requiredError: Error = None,
		schemeError: Error = None,
		tokenUrl: str = None,
		refreshUrl: str = None,
	):
		super().__init__(
			type=OAuth2Type.Password,
			scheme=scheme,
			auth=auth,
			optional=optional,
			requiredError=requiredError,
			schemeError=schemeError,
			tokenUrl=tokenUrl,
			refreshUrl=refreshUrl,
		)
		return


class OAuth2ClientCredentials(OAuth2):
	def __init__(
		self,
		scheme: str,
		auth: Authorization,
		optional: bool = False,
		requiredError: Error = None,
		schemeError: Error = None,
		tokenUrl: str = None,
		refreshUrl: str = None,
	):
		super().__init__(
			type=OAuth2Type.ClientCredentials,
			scheme=scheme,
			auth=auth,
			optional=optional,
			requiredError=requiredError,
			schemeError=schemeError,
			tokenUrl=tokenUrl,
			refreshUrl=refreshUrl,
		)
		return


class OAuth2AuthorizationCode(OAuth2):
	def __init__(
		self,
		scheme: str,
		auth: Authorization,
		optional: bool = False,
		requiredError: Error = None,
		schemeError: Error = None,
		authorizationUrl: str = None,
		tokenUrl: str = None,
	):
		super().__init__(
			type=OAuth2Type.AuthorizationCode,
			scheme=scheme,
			auth=auth,
			optional=optional,
			requiredError=requiredError,
			schemeError=schemeError,
			authorizationUrl=authorizationUrl,
			tokenUrl=tokenUrl,
		)
		return