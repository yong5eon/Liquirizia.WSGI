# -*- coding: utf-8 -*-

from .RequestRunner import RequestRunner, RequestFilter, ResponseFilter
from .RequestStreamRunner import RequestStreamRunner
from .RequestServerSentEventsRunner import RequestServerSentEventsRunner
from .RequestWebSocketRunner import RequestWebSocketRunner
from ..Validators import (
	Origin,
	Auth,
	Parameter,
	QueryString,
	Header,
	QueryString,
	Body,
)
from ..Authorizations import (
	Query as QueryAuth,
	Cookie as CookieAuth,
	Header as HeaderAuth,
	HTTP as HTTPAuth,
	OAuth2Implicit as OAuth2ImplicitAuth,
	OAuth2Password as OAuth2PasswordAuth,
	OAuth2ClientCredentials as OAuth2ClientCredentialsAuth,
	OAuth2AuthorizationCode as OAuth2AuthorizationCodeAuth,
)
from ..Router import Router
from ..Description import (
	Descriptor,
	Description,
	Response,
	Body as BodyDescription,
	Content as ContentDescription,
	Auth as Authenticate,
)
from ..Description.Auth import (
	HTTP as HTTPAuthenticate,
	Cookie as CookieAuthenticate,
	Header as HeaderAuthenticate,
	Query as QueryAuthenticate,
	OAuth2 as OAuth2Authenticate,
)
from typing import Type, Sequence, Union

__all__ = (
	'RequestProperties',
	'RequestStreamProperties',
	'RequestServerSentEventsProperties',
	'RequestWebSocketProperties',
)


class RequestProperties(object):
	"""Request Decorator Class for RequestRunner"""
	def __init__(
		self,
		method: str,
		url: str,
		origin: Union[Origin, Sequence[Origin]] = None,
		auth: Auth = None,
		parameter: Parameter = None,
		qs: QueryString = None,
		header: Header = None,
		body: Body = None,
		response: Union[Response, Sequence[Response]] = None,
		summary: str = None,
		description: str = None,
		tags: Union[str, Sequence[str]] = None,
		onRequest: Union[RequestFilter, Sequence[RequestFilter]] = None,
		onResponse : Union[ResponseFilter, Sequence[ResponseFilter]] = None,
	):
		self.method = method
		self.url = url
		self.origin = origin
		self.auth = auth
		self.parameter = parameter
		self.qs = qs
		self.header = header
		self.body = body 
		self.response = response
		self.onRequest = onRequest
		self.onResponse = onResponse
		self.summary = summary
		self.description = description
		self.tags = tags
		return
	def __call__(self, obj: Type[RequestRunner]):
		from ..Runners import RunRequest
		router = Router()
		router.add(RunRequest(
			obj=obj,
			method=self.method,
			url=self.url,
			origin=self.origin,
			auth=self.auth,
			parameter=self.parameter,
			qs=self.qs,
			header=self.header,
			body=self.body,
			onRequest=self.onRequest,
			onResponse=self.onResponse,
		))
		descriptor = Descriptor()
		auth = None
		if self.auth:
			if isinstance(self.auth, HTTPAuth):
				auth = Authenticate(
					name=self.auth.__class__.__name__,
					format=HTTPAuthenticate(
						format=self.auth.scheme,
						bearerFormat=self.auth.format,
					),
					optional=self.auth.optional,
				)
			if isinstance(self.auth, CookieAuth):
				auth = Authenticate(
					name=self.auth.__class__.__name__,
					format=CookieAuthenticate(
						name=self.auth.name,
					),
					optional=self.auth.optional,
				)
			if isinstance(self.auth, HeaderAuth):
				auth = Authenticate(
					name=self.auth.__class__.__name__,
					format=HeaderAuthenticate(
						name=self.auth.name,
					),
					optional=self.auth.optional,
				)
			if isinstance(self.auth, QueryAuth):
				auth = Authenticate(
					name=self.auth.__class__.__name__,
					format=QueryAuthenticate(
						name=self.auth.name,
					),
					optional=self.auth.optional,
				)
			if isinstance(self.auth, (
				OAuth2ImplicitAuth,
				OAuth2PasswordAuth,
				OAuth2ClientCredentialsAuth,
				OAuth2AuthorizationCodeAuth,
			)):
				auth = Authenticate(
					name=self.auth.__class__.__name__,
					format=OAuth2Authenticate(
						type=str(self.auth.type),
						**self.auth.kwargs,
					),
					optional=self.auth.optional,
				)
		contents = []
		if self.body:
			contents.append(ContentDescription(
				format=self.body.type,
				schema=self.body.format,
				example=self.body.example,
			))
		descriptor.add(Description(
			method=self.method,
			url=self.url,
			auth=auth,
			parameters=self.parameter.format if self.parameter else None,
			qs=self.qs.format if self.qs else None,
			headers=self.header.format if self.header else None,
			body=BodyDescription(
				content=contents,
				required=self.body.required,
			) if self.body else None,
			responses=self.response,
			summary=self.summary,
			description=self.description,
			tags=self.tags,
		))
		return obj


class RequestStreamProperties(object):
	"""Request Properties Decorator Class for RequestStreamRunner"""
	def __init__(
		self,
		method: str,
		url: str,
		origin: Union[Origin, Sequence[Origin]] = None,
		auth: Auth = None,
		parameter: Parameter = None,
		qs: QueryString = None,
		header: Header = None,
		response: Union[Response, Sequence[Response]] = None,
		summary: str = None,
		description: str = None,
		tags: Union[str, Sequence[str]] = None,
	):
		self.method = method
		self.url = url
		self.origin = origin
		self.auth = auth
		self.parameter = parameter
		self.qs = qs
		self.header = header
		self.response = response
		self.summary = summary
		self.description = description
		self.tags = tags
		return
	def __call__(self, obj: Type[RequestStreamRunner]):
		from ..Runners import RunRequestStream
		router = Router()
		router.add(RunRequestStream(
			obj=obj,
			method=self.method,
			url=self.url,
			origin=self.origin,
			auth=self.auth,
			parameter=self.parameter,
			qs=self.qs,
			header=self.header,
		))
		descriptor = Descriptor()
		auth = None
		if self.auth:
			if isinstance(self.auth, HTTPAuth):
				auth = Authenticate(
					name=self.auth.__class__.__name__,
					format=HTTPAuthenticate(
						format=self.auth.scheme,
						bearerFormat=self.auth.format,
					),
					optional=self.auth.optional,
				)
			if isinstance(self.auth, CookieAuth):
				auth = Authenticate(
					name=self.auth.__class__.__name__,
					format=CookieAuthenticate(
						name=self.auth.name,
					),
					optional=self.auth.optional,
				)
			if isinstance(self.auth, HeaderAuth):
				auth = Authenticate(
					name=self.auth.__class__.__name__,
					format=HeaderAuthenticate(
						name=self.auth.name,
					),
					optional=self.auth.optional,
				)
			if isinstance(self.auth, QueryAuth):
				auth = Authenticate(
					name=self.auth.__class__.__name__,
					format=QueryAuthenticate(
						name=self.auth.name,
					),
					optional=self.auth.optional,
				)
			if isinstance(self.auth, OAuth2Auth):
				auth = Authenticate(
					name='{}{}'.format(self.auth.__class__.__name__, str(self.auth.type)),
					format=OAuth2Authenticate(
						type=str(self.auth.type),
						**self.auth.kwargs,
					),
					optional=self.auth.optional,
				)
		descriptor.add(Description(
			method=self.method,
			url=self.url,
			auth=auth,
			parameters=self.parameter.format if self.parameter else None,
			qs=self.qs.format if self.qs else None,
			headers=self.header.format if self.header else None,
			responses=self.response,
			summary=self.summary,
			description=self.description,
			tags=self.tags,
		))
		return obj


class RequestServerSentEventsProperties(object):
	"""Request Properties Decorator Class for RequestServerSentEventsRunner"""
	def __init__(
		self,
		method: str,
		url: str,
		origin: Union[Origin, Sequence[Origin]] = None,
		auth: Auth = None,
		parameter: Parameter = None,
		qs: QueryString = None,
		header: Header = None,
		response: Union[Response, Sequence[Response]] = None,
		summary: str = None,
		description: str = None,
		tags: Union[str, Sequence[str]] = None,
	):
		self.method = method
		self.url = url
		self.origin = origin
		self.auth = auth
		self.parameter = parameter
		self.qs = qs
		self.header = header
		self.response = response
		self.summary = summary
		self.description = description
		self.tags = tags
		return
	def __call__(self, obj: Type[RequestServerSentEventsRunner]):
		from ..Runners import RunRequestServerSentEvents
		router = Router()
		router.add(RunRequestServerSentEvents(
			obj=obj,
			method=self.method,
			url=self.url,
			origin=self.origin,
			auth=self.auth,
			parameter=self.parameter,
			qs=self.qs,
			header=self.header,
		))
		descriptor = Descriptor()
		auth = None
		if self.auth:
			if isinstance(self.auth, HTTPAuth):
				auth = Authenticate(
					name=self.auth.__class__.__name__,
					format=HTTPAuthenticate(
						format=self.auth.scheme,
						bearerFormat=self.auth.format,
					),
					optional=self.auth.optional,
				)
			if isinstance(self.auth, CookieAuth):
				auth = Authenticate(
					name=self.auth.__class__.__name__,
					format=CookieAuthenticate(
						name=self.auth.name,
					),
					optional=self.auth.optional,
				)
			if isinstance(self.auth, Header):
				auth = Authenticate(
					name=self.auth.__class__.__name__,
					format=HeaderAuthenticate(
						name=self.auth.name,
					),
					optional=self.auth.optional,
				)
			if isinstance(self.auth, QueryAuth):
				auth = Authenticate(
					name=self.auth.__class__.__name__,
					format=QueryAuthenticate(
						name=self.auth.name,
					),
					optional=self.auth.optional,
				)
			if isinstance(self.auth, OAuth2Auth):
				auth = Authenticate(
					name='{}{}'.format(self.auth.__class__.__name__, str(self.auth.type)),
					format=OAuth2Authenticate(
						type=str(self.auth.type),
						**self.auth.kwargs,
					),
					optional=self.auth.optional,
				)
		descriptor.add(Description(
			method=self.method,
			url=self.url,
			auth=auth,
			parameters=self.parameter.format if self.parameter else None,
			qs=self.qs.format if self.qs else None,
			headers=self.header.format if self.header else None,
			responses=self.response,
			summary=self.summary,
			description=self.description,
			tags=self.tags,
		))
		return obj


class RequestWebSocketProperties(object):
	"""Request Properties Decorator Class for RequestWebSocketRunner"""
	def __init__(
		self,
		method: str,
		url: str,
		origin: Union[Origin, Sequence[Origin]] = None,
		auth: Auth = None,
		parameter: Parameter = None,
		qs: QueryString = None,
		header: Header = None,
		response: Union[Response, Sequence[Response]] = None,
		summary: str = None,
		description: str = None,
		tags: Union[str, Sequence[str]] = None,
	):
		self.method = method
		self.url = url
		self.origin = origin
		self.auth = auth
		self.parameter = parameter
		self.qs = qs
		self.header = header
		self.response = response
		self.summary = summary
		self.description = description
		self.tags = tags
		return
	def __call__(self, obj: Type[RequestWebSocketRunner]):
		from ..Runners import RunRequestWebSocket
		router = Router()
		router.add(RunRequestWebSocket(
			obj=obj,
			url=self.url,
			origin=self.origin,
			auth=self.auth,
			parameter=self.parameter,
			qs=self.qs,
			header=self.header,
		))
		descriptor = Descriptor()
		auth = None
		if self.auth:
			if isinstance(self.auth, HTTPAuth):
				auth = Authenticate(
					name=self.auth.__class__.__name__,
					format=HTTPAuthenticate(
						format=self.auth.scheme,
						bearerFormat=self.auth.format,
					),
					optional=self.auth.optional,
				)
			if isinstance(self.auth, CookieAuth):
				auth = Authenticate(
					name=self.auth.__class__.__name__,
					format=CookieAuthenticate(
						name=self.auth.name,
					),
					optional=self.auth.optional,
				)
			if isinstance(self.auth, HeaderAuth):
				auth = Authenticate(
					name=self.auth.__class__.__name__,
					format=HeaderAuthenticate(
						name=self.auth.name,
					),
					optional=self.auth.optional,
				)
			if isinstance(self.auth, QueryAuth):
				auth = Authenticate(
					name=self.auth.__class__.__name__,
					format=QueryAuthenticate(
						name=self.auth.name,
					),
					optional=self.auth.optional,
				)
			if isinstance(self.auth, OAuth2Auth):
				auth = Authenticate(
					name='{}{}'.format(self.auth.__class__.__name__, str(self.auth.type)),
					format=OAuth2Authenticate(
						type=str(self.auth.type),
						**self.auth.kwargs,
					),
					optional=self.auth.optional,
				)
		descriptor.add(Description(
			method=self.method,
			url=self.url,
			auth=auth,
			parameters=self.parameter.format if self.parameter else None,
			qs=self.qs.format if self.qs else None,
			headers=self.header.format if self.header else None,
			responses=self.response,
			summary=self.summary,
			description=self.description,
			tags=self.tags,
		))
		return obj

