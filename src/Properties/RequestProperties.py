# -*- coding: utf-8 -*-

from re import A
from .RequestRunner import RequestRunner, RequestFilter, ResponseFilter
from .RequestStreamRunner import RequestStreamRunner
from .RequestServerSentEventsRunner import RequestServerSentEventsRunner
from .RequestWebSocketRunner import RequestWebSocketRunner
from .Validators import (
	Origin,
	Auth,
	Parameters,
	QueryString,
	Headers,
	QueryString,
	Body,
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
		parameters: Parameters = None,
		qs: QueryString = None,
		headers: Headers = None,
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
		self.parameters = parameters
		self.qs = qs
		self.headers = headers
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
			parameters=self.parameters,
			qs=self.qs,
			headers=self.headers,
			body=self.body,
			onRequest=self.onRequest,
			onResponse=self.onResponse,
		))
		descriptor = Descriptor()
		auth = None
		if self.auth:
			auth = Authenticate(
				name=self.auth.credentials.name,
				format=self.auth.credentials.format,
				optional=self.auth.optional,
			)
		contents = []
		if self.body and self.body.content:
			for content in self.body.content:
				contents.append(ContentDescription(
					format=content.format,
					schema=content.schema,
					example=content.example,
				))
		descriptor.add(Description(
			method=self.method,
			url=self.url,
			auth=auth,
			parameters=self.parameters.format if self.parameters else None,
			qs=self.qs.format if self.qs else None,
			headers=self.headers.format if self.headers else None,
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
		parameters: Parameters = None,
		qs: QueryString = None,
		headers: Headers = None,
		response: Union[Response, Sequence[Response]] = None,
		summary: str = None,
		description: str = None,
		tags: Union[str, Sequence[str]] = None,
	):
		self.method = method
		self.url = url
		self.origin = origin
		self.auth = auth
		self.parameters = parameters
		self.qs = qs
		self.headers = headers
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
			parameters=self.parameters,
			qs=self.qs,
			headers=self.headers,
		))
		descriptor = Descriptor()
		auth = None
		if self.auth:
			auth = Authenticate(
				name=self.auth.credentials.name,
				format=self.auth.credentials.format,
				optional=self.auth.optional,
			)
		descriptor.add(Description(
			method=self.method,
			url=self.url,
			auth=auth,
			parameters=self.parameters.format if self.parameters else None,
			qs=self.qs.format if self.qs else None,
			headers=self.headers.format if self.headers else None,
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
		parameters: Parameters = None,
		qs: QueryString = None,
		headers: Headers = None,
		response: Union[Response, Sequence[Response]] = None,
		summary: str = None,
		description: str = None,
		tags: Union[str, Sequence[str]] = None,
	):
		self.method = method
		self.url = url
		self.origin = origin
		self.auth = auth
		self.parameters = parameters
		self.qs = qs
		self.headers = headers
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
			parameters=self.parameters,
			qs=self.qs,
			headers=self.headers,
		))
		descriptor = Descriptor()
		auth = None
		if self.auth:
			auth = Authenticate(
				name=self.auth.credentials.name,
				format=self.auth.credentials.format,
				optional=self.auth.optional,
			)
		descriptor.add(Description(
			method=self.method,
			url=self.url,
			auth=auth,
			parameters=self.parameters.format if self.parameters else None,
			qs=self.qs.format if self.qs else None,
			headers=self.headers.format if self.headers else None,
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
		parameters: Parameters = None,
		qs: QueryString = None,
		headers: Headers = None,
		response: Union[Response, Sequence[Response]] = None,
		summary: str = None,
		description: str = None,
		tags: Union[str, Sequence[str]] = None,
	):
		self.method = method
		self.url = url
		self.origin = origin
		self.auth = auth
		self.parameters = parameters
		self.qs = qs
		self.headers = headers
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
			parameters=self.parameters,
			qs=self.qs,
			headers=self.headers,
		))
		descriptor = Descriptor()
		auth = None
		if self.auth:
			auth = Authenticate(
				name=self.auth.credentials.name,
				format=self.auth.credentials.format,
				optional=self.auth.optional,
			)
		descriptor.add(Description(
			method=self.method,
			url=self.url,
			auth=auth,
			parameters=self.parameters.format if self.parameters else None,
			qs=self.qs.format if self.qs else None,
			headers=self.headers.format if self.headers else None,
			responses=self.response,
			summary=self.summary,
			description=self.description,
			tags=self.tags,
		))
		return obj

