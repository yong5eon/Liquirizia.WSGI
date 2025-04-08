# -*- coding: utf-8 -*-

from .RequestRunner import RequestRunner
from .RequestStreamRunner import RequestStreamRunner
from .RequestServerSentEventsRunner import RequestServerSentEventsRunner
from .RequestWebSocketRunner import RequestWebSocketRunner
from .Validator import (
	Origin,
	Auth,
	Parameter,
	QueryString,
	Header,
	QueryString,
	Body,
)
from ..Router import Router
from ..Filters import (
	RequestFilter,
	ResponseFilter,
)
from ..Description import (
	Descriptor,
	Description,
	Response,
	Body as BodyDescription,
	Content as ContentDescription,
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
		summary: str = None,
		description: str = None,
		tags: Union[str, Sequence[str]] = None,
		response: Response = None,
		onRequest: RequestFilter = None,
		onResponse : ResponseFilter = None,
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
		from ..Routes import RouteRequest
		router = Router()
		router.add(RouteRequest(
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
		contents = []
		for format, _ in self.body.decoders.items() if self.body else []:
			contents.append(ContentDescription(
				format=format,
				schema=self.body.format,
			))
		descriptor.add(Description(
			summary=self.summary,
			description=self.description,
			tags=self.tags,
			method=self.method,
			url=self.url,
			# auth=self.auth,
			parameters=self.parameter.format if self.parameter else None,
			qs=self.qs.format if self.qs else None,
			headers=self.header.format if self.header else None,
			body=BodyDescription(
				content=contents,
				required=self.body.required,
			) if self.body else None,
			responses=self.response,
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
		return
	
	def __call__(self, obj: Type[RequestStreamRunner]):
		from ..Routes import RouteRequestStream
		router = Router()
		router.add(RouteRequestStream(
			obj=obj,
			method=self.method,
			url=self.url,
			origin=self.origin,
			auth=self.auth,
			parameter=self.parameter,
			qs=self.qs,
			header=self.header,
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
		return
	
	def __call__(self, obj: Type[RequestServerSentEventsRunner]):
		from ..Routes import RouteRequestServerSentEvents
		router = Router()
		router.add(RouteRequestServerSentEvents(
			obj=obj,
			method=self.method,
			url=self.url,
			origin=self.origin,
			auth=self.auth,
			parameter=self.parameter,
			qs=self.qs,
			header=self.header,
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
		return
	
	def __call__(self, obj: Type[RequestWebSocketRunner]):
		from ..Routes import RouteRequestWebSocket
		router = Router()
		router.add(RouteRequestWebSocket(
			obj=obj,
			url=self.url,
			origin=self.origin,
			auth=self.auth,
			parameter=self.parameter,
			qs=self.qs,
			header=self.header,
		))
		return obj

