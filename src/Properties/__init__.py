# -*- coding: utf-8 -*-

from .RequestRunner import RequestRunner
from .RequestStreamRunner import RequestStreamRunner
from .RequestServerSentEventsRunner import RequestServerSentEventsRunner
from .RequestWebSocketRunner import RequestWebSocketRunner
from .Properties import Properties

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
from ..Description import Description

from Liquirizia.Validator import Validator

from typing import Type, Union, Dict

__all__ = (
	'RequestRunner',
	'RequestStreamRunner',
	'RequestServerSentEventsRunner',
	'RequestWebSocketRunner',
	'RequestProperties',
	'Properties',
)


class RequestProperties(object):
	"""Request Properties Decorator Class"""
	def __init__(
		self,
		method: str,
		url: str,
		parameter: Validator = None,
		header: Validator = None,
		qs: Validator = None,
		body: Validator = None,
		bodyParsers: Dict[str, Parser] = {
			'application/x-www-form-urlencoded': FormUrlEncodedParser(),
			'application/x-www-form': FormUrlEncodedParser(),
			'form-urlencoded': FormUrlEncodedParser(),
			'form': FormUrlEncodedParser(),
			'application/json': JavaScriptObjectNotationParser(),
			'json': JavaScriptObjectNotationParser(),
		},
		onRequest: RequestFilter = None,
		onResponse : ResponseFilter = None,
		cors: CORS = CORS(),
		description: Description = None,
	):
		self.method = method
		self.url = url
		self.parameter = parameter
		self.header = header
		self.qs = qs
		self.body = body
		self.bodyParsers = bodyParsers
		self.onRequest = onRequest
		self.onResponse = onResponse
		self.cors = cors
		self.description = description
		return
	
	def __call__(self, obj: Type[Union[RequestRunner,RequestStreamRunner,RequestServerSentEventsRunner,RequestWebSocketRunner]]):
		obj.__properties__ = Properties(
			method=self.method,
			url=self.url,
		)
		router = Router()
		if issubclass(obj, RequestRunner):
			router.add(RouteRequest(
				obj=obj,
				method=self.method,
				url=self.url,
				parameter=self.parameter,
				header=self.header,
				qs=self.qs,
				body=self.body,
				bodyParsers=self.bodyParsers,
				onRequest=self.onRequest,
				onResponse=self.onResponse,
				cors=self.cors
			))
			return obj
		if issubclass(obj, RequestStreamRunner):
			router.add(RouteRequestStream(
				obj=obj,
				method=self.method,
				url=self.url,
				parameter=self.parameter,
				header=self.header,
				qs=self.qs,
				cors=self.cors
			))
			return obj
		if issubclass(obj, RequestServerSentEventsRunner):
			router.add(RouteRequestServerSentEvents(
				obj=obj,
				method=self.method,
				url=self.url,
				parameter=self.parameter,
				header=self.header,
				qs=self.qs,
				cors=self.cors
			))
			return obj
		if issubclass(obj, RequestWebSocketRunner):
			router.add(RouteRequestWebSocket(
				obj=obj,
				url=self.url,
				parameter=self.parameter,
				header=self.header,
				qs=self.qs,
				cors=self.cors,
			))
			return obj
		raise RuntimeError('{} is not support type'.format(obj.__name__))
