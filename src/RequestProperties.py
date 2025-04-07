# -*- coding: utf-8 -*-

from .Properties import (
	RequestRunner,
	RequestStreamRunner,
	RequestServerSentEventsRunner,
	RequestWebSocketRunner,
)
from .Validator import (
	Origin,
	Auth,
	Parameter,
	QueryString,
	Header,
	QueryString,
	Body,
)
from .Router import Router
from .Routes import (
	RouteRequest,
	RouteRequestStream,
	RouteRequestServerSentEvents,
	RouteRequestWebSocket,
)
from .Filters import (
	RequestFilter,
	ResponseFilter,
)
from .Description import Response
from typing import Type, Sequence, Union

__all__ = (
	'RequestProperties',
	'RequestStreamProperties',
	'RequestServerSentEventsProperties',
	'RequestWebSocketProperties',
)


class RequestProperties(object):
	"""Request Properties Decorator Class for RequestRunner"""
	"""
	Declare Request
	----------------------------------------------------------------------------
	@RequestProperties(
		method='...',
		url='/api/sample/:a/:b/:c',
		origin=Origin('https://xxx.com'),
		auth=Http(
			scheme='Bearer',
			format='JWT',
			auth=SampleAuthorization(),
		),
		parameter=Parameter(
			{
				'a': IsString(),
				'b': ToInteger(required=False),
				'c': ToNumber(required=False),
			},
			schema={
				'a': String(),
				'b': Integer(required=False),
				'c': Number(required=False),
			},
		),
		qs=QueryString(
			{
				'a': IsString(),
				'b': ToInteger(required=False),
				'c': ToFloat(required=False),
			},
			requires=['a'],
			requiresError=BadRequestError('a is required'),
			schema={
				'a': String(),
				'b': Integer(required=False),
				'c': Number(required=False),
			},
		),
		header=Header(
			{
				'X-Custom-Header': IsString(),
			},
			requires=['Authorization'],
			requiresError=Error('Authorization header is required'),
			schema={
				'X-Custom-Header': String(),
			},
		),
		body=Body(
			content=(
				Content(
					decode=JavaScriptObjectNotationDecoder(),
					va=IsObject(
						{
							'a': IsString(),
							'b': IsInteger(required=False),
							'c': IsNumber(required=False),
						},
						requres=['a'],
						required=False,
						requresError=BadRequestError('a is required'),
						requredError=BadRequestError('body is required'),
						error=BadRequestError('Invalid JSON'),
					),
					format='application/json',
					schema=Object(
						properties={
							'a': IsString(),
							'b': IsInteger(required=False),
							'c': IsNumber(required=False),
						},
						required=False,
					),
				),
				Content(
					decode=FormUrlEncodedDecoder(),
					va=IsObject(
						required=False,
					),
					requres=['a'],
					requresError=BadRequestError('a is required'),
					error=BadRequestError('Invalid FormUrlEncoded'),
					format='application/x-www-form-urlencoded',
					schema=Object(
						properties={
							'a': IsString(),
							'b': IsInteger(required=False),
							'c': IsNumber(required=False),
						},
						required=False,
					),
				),
			),
			error=BadRequestError('Unsupported media type'),
		},
		response=(
			Response(
				status=200,
				description='성공',
				content=Content(
					format='application/json',
					schema=Object(),
				),
			),
			Response(
				status=400,
				description='실패',
				content=Content(
					format='text/plain',
				),
			),
			...
		),
		onRequest=SampleRequest(),
		onResponse=SampleResponse(),
	)
	class SampleRequest(RequestRunner):
		...
	"""
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
		return
	
	def __call__(self, obj: Type[RequestRunner]):
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

