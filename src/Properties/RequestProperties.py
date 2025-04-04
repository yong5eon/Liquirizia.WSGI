# -*- coding: utf-8 -*-

from .RequestRunner import RequestRunner
from .RequestStreamRunner import RequestStreamRunner
from .RequestServerSentEventsRunner import RequestServerSentEventsRunner
from .RequestWebSocketRunner import RequestWebSocketRunner
from .Properties import Properties
from .Validator import (
	Parameter,
	Header,
	QueryString,
	Content,
)

from ..Router import Router
from ..Routes import *
from ..Filters import (
	RequestFilter,
	ResponseFilter,
)
from ..Decoder import Decoder
from ..Decoders import (
	TextDecoder,
	FormUrlEncodedDecoder,
	JavaScriptObjectNotationDecoder
)
from ..CORS import CORS

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
		auth=Http(
			scheme='Bearer',
			format='JWT',
			auth=SampleAuthorization(),
		),
		parameter=Parameter(
			va={
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
			va={
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
			va={
				'X-Custom-Header': IsString(),
			},
			requires=['Authorization'],
			requiresError=Error('Authorization header is required'),
			schema={
				'X-Custom-Header': String(),
			},
		),
		body=Body(
			content=Content(
				va=IsObject(
					required=False,
				),
				requres=['a'],
				requresError=BadRequestError('a is required'),
				error=BadRequestError('Invalid JSON'),
				decode=JavaScriptObjectNotationDecoder(),
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
			content=Content(
				format='application/x-www-form-urlencoded',
				schema=Object(
					properties={
						'a': IsString(),
						'b': IsInteger(required=False),
						'c': IsNumber(required=False),
					},
					required=False,
				),
				decoder=FormUrlEncodedDecoder(),
				va=IsObject(
					required=False,
				),
				requres=['a'],
				requresError=BadRequestError('a is required'),
				error=BadRequestError('Invalid FormUrlEncoded'),
			),
		),
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
		origin='*',
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
		parameter: Parameter = None,
		qs: QueryString = None,
		header: Header = None,
		body = None,
		auth = None,
		origin: Union[str, Sequence[str]] = None,
		onRequest: RequestFilter = None,
		onResponse : ResponseFilter = None,
		respones = None,
	):
		self.method = method
		self.url = url
		self.cors = cors
		self.parameter = parameter
		self.header = header
		self.qs = qs
		self.content = content
		self.contentParsers = contentParsers
		self.onRequest = onRequest
		self.onResponse = onResponse
		return
	
	def __call__(self, obj: Type[RequestRunner]):
		obj.__properties__ = Properties(
			method=self.method,
			url=self.url,
		)
		router = Router()
		router.add(RouteRequest(
			obj=obj,
			method=self.method,
			url=self.url,
			cors=self.cors,
			parameter=self.parameter,
			header=self.header,
			qs=self.qs,
			content=self.content,
			contentParsers=self.contentParsers,
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
		cors: CORS = CORS(),
		parameter: Parameter = None,
		header: Header = None,
		qs: QueryString = None,
		onRequest: RequestFilter = None,
	):
		self.method = method
		self.url = url
		self.cors = cors
		self.parameter = parameter
		self.header = header
		self.qs = qs
		self.onRequest = onRequest
		return
	
	def __call__(self, obj: Type[RequestStreamRunner]):
		obj.__properties__ = Properties(
			method=self.method,
			url=self.url,
		)
		router = Router()
		router.add(RouteRequestStream(
			obj=obj,
			method=self.method,
			url=self.url,
			cors=self.cors,
			parameter=self.parameter,
			header=self.header,
			qs=self.qs,
			onRequest=self.onRequest,
		))
		return obj

class RequestServerSentEventsProperties(object):
	"""Request Properties Decorator Class for RequestServerSentEventsRunner"""
	def __init__(
		self,
		method: str,
		url: str,
		cors: CORS = CORS(),
		parameter: Parameter = None,
		header: Header = None,
		qs: QueryString = None,
		onRequest: RequestFilter = None,
	):
		self.method = method
		self.url = url
		self.cors = cors
		self.parameter = parameter
		self.header = header
		self.qs = qs
		self.onRequest = onRequest
		return
	
	def __call__(self, obj: Type[RequestServerSentEventsRunner]):
		obj.__properties__ = Properties(
			method=self.method,
			url=self.url,
		)
		router = Router()
		router.add(RouteRequestServerSentEvents(
			obj=obj,
			method=self.method,
			url=self.url,
			cors=self.cors,
			parameter=self.parameter,
			header=self.header,
			qs=self.qs,
			onRequest=self.onRequest,
		))
		return obj


class RequestWebSocketProperties(object):
	"""Request Properties Decorator Class for RequestWebSocketRunner"""
	def __init__(
		self,
		method: str,
		url: str,
		cors: CORS = CORS(),
		parameter: Parameter = None,
		header: Header = None,
		qs: QueryString = None,
		onRequest: RequestFilter = None,
	):
		self.method = method
		self.url = url
		self.cors = cors
		self.parameter = parameter
		self.header = header
		self.qs = qs
		self.onRequest = onRequest
		return
	
	def __call__(self, obj: Type[RequestWebSocketRunner]):
		obj.__properties__ = Properties(
			method=self.method,
			url=self.url,
		)
		router = Router()
		router.add(RouteRequestWebSocket(
			obj=obj,
			url=self.url,
			cors=self.cors,
			parameter=self.parameter,
			header=self.header,
			qs=self.qs,
			onRequest=self.onRequest,
		))
		return obj

