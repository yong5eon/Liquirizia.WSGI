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
from ..Parser import (
	Parser,
	FormUrlEncodedParser,
	JavaScriptObjectNotationParser,
)
from ..CORS import CORS

from typing import Type, Dict, Union

__all__ = (
	'RequestProperties',
	'RequestStreamProperties',
	'RequestServerSentEventsProperties',
	'RequestWebSocketProperties',
)


class RequestProperties(object):
	"""Request Properties Decorator Class for RequestRunner"""
	def __init__(
		self,
		method: str,
		url: str,
		cors: CORS = CORS(),
		parameter: Parameter = None,
		header: Header = None,
		qs: QueryString = None,
		content: Content = None,
		contentParsers: Dict[str, Parser] = {
			'application/x-www-form-urlencoded': FormUrlEncodedParser(),
			'application/x-www-form': FormUrlEncodedParser(),
			'form-urlencoded': FormUrlEncodedParser(),
			'form': FormUrlEncodedParser(),
			'application/json': JavaScriptObjectNotationParser(),
			'json': JavaScriptObjectNotationParser(),
		},
		onRequest: RequestFilter = None,
		onResponse : ResponseFilter = None,
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
	):
		self.method = method
		self.url = url
		self.cors = cors
		self.parameter = parameter
		self.header = header
		self.qs = qs
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
	):
		self.method = method
		self.url = url
		self.cors = cors
		self.parameter = parameter
		self.header = header
		self.qs = qs
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
	):
		self.method = method
		self.url = url
		self.cors = cors
		self.parameter = parameter
		self.header = header
		self.qs = qs
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
		))
		return obj

