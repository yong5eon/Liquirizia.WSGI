# -*- coding: utf-8 -*-

from .Validators import Credentials
from ..Request import Request
from ..Headers import (
	Authorization,
	Cookie as CookieObject,
)
from ..Description.Auth import (
	Query as QueryFormat,
	Cookie as CookieFormat,
	Header as HeaderFormat,
	HTTP as HTTPFormat,
	OAuth2 as OAuth2Format,
)
from typing import List, Any

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


class Query(Credentials):
	def __init__(
		self,
		name: str,
	):
		self.key = name
		return
	def __call__(self, request: Request) -> Any:
		if not hasattr(request.qs, self.key):
			return
		return getattr(request.qs, self.key)
	@property
	def name(self) -> str: return 'Query'
	@property
	def format(self) -> QueryFormat:
		return QueryFormat(
			name=self.key,
		)


class Cookie(Credentials):
	def __init__(
		self,
		name: str,
	):
		self.key = name
		return
	def __call__(self, request: Request) -> Any:
		cookies: List[CookieObject] = request.header('Cookie')
		if not cookies:
			return
		_ = None
		for cookie in cookies:
			if cookie.name == self.key:
				_ = cookie
				break
		return _
	@property
	def name(self) -> str: return 'Cookie'
	@property
	def format(self) -> CookieFormat:
		return CookieFormat(
			name=self.key,
		)


class Header(Credentials):
	def __init__(
		self,
		name: str,
	):
		self.key = name
		return
	def __call__(self, request: Request) -> Any:
		return request.header(self.name)
	@property
	def name(self) -> str: return 'Header'
	@property
	def format(self) -> HeaderFormat:
		return HeaderFormat(
			name=self.key,
		)


class HTTP(Credentials):
	def __init__(
		self,
		scheme: str,
		format: str = None,
	):
		self.scheme = scheme
		self.fmt = format
		return
	def __call__(self, request: Request) -> Authorization:
		return request.header('Authorization')
	@property
	def name(self) -> str: return 'HTTP'
	@property
	def format(self) -> HTTPFormat:
		return HTTPFormat(
			format=self.scheme,
			bearerFormat=self.fmt,
		)


class OAuth2Implicit(Credentials):
	def __init__(
		self,
		authorizationUrl: str = None,
	):
		self.authorizationUrl = authorizationUrl
		return
	def __call__(self, request: Request) -> Authorization:
		return request.header('Authorization')
	@property
	def name(self) -> str: return 'OAuth2Implicit'
	@property
	def format(self) -> OAuth2Format:
		return OAuth2Format(
			type='implicit',
			authorizationUrl=self.authorizationUrl,
		)


class OAuth2Password(Credentials):
	def __init__(
		self,
		tokenUrl: str = None,
		refreshUrl: str = None,
	):
		self.tokenUrl = tokenUrl
		self.refreshUrl = refreshUrl
		return
	def __call__(self, request: Request) -> Authorization:
		return request.header('Authorization')
	@property
	def name(self) -> str: return 'OAuth2Password'
	@property
	def format(self) -> OAuth2Format:
		return OAuth2Format(
			type='password',
			tokenUrl=self.tokenUrl,
			refreshUrl=self.refreshUrl,
		)


class OAuth2ClientCredentials(Credentials):
	def __init__(
		self,
		tokenUrl: str = None,
		refreshUrl: str = None,
	):
		self.tokenUrl = tokenUrl
		self.refreshUrl = refreshUrl
		return
	def __call__(self, request: Request) -> Authorization:
		return request.header('Authorization')
	@property
	def name(self) -> str: return 'OAuth2ClientCredentials'
	@property
	def format(self) -> OAuth2Format:
		return OAuth2Format(
			type='clientCredentials',
			tokenUrl=self.tokenUrl,
			refreshUrl=self.refreshUrl,
		)


class OAuth2AuthorizationCode(Credentials):
	def __init__(
		self,
		authorizationUrl: str = None,
		tokenUrl: str = None,
	):
		self.authorizationUrl = authorizationUrl
		self.tokenUrl = tokenUrl
		return
	def __call__(self, request: Request) -> Authorization:
		return request.header('Authorization')
	@property
	def name(self) -> str: return 'OAuth2AuthorizationCode'
	@property
	def format(self) -> OAuth2Format:
		return OAuth2Format(
			type='authorizationCode',
			authorizationUrl=self.authorizationUrl,
			tokenUrl=self.tokenUrl,
		)
