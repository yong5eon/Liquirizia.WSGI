# -*- coding: utf-8 -*-

from .Router import Router
from .Routes import *
from .Properties import *
from .Filters import (
	RequestFilter,
	ResponseFilter,
)
from .CORS import CORS
from .Description import Description

from Liquirizia.Validator import Validator

from typing import Union

__all__ = (
	'RequestProperties',
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
		onRequest: RequestFilter = None,
		onResponse : ResponseFilter = None,
		cors: CORS = None,
		description: Description = None,
	):
		self.method = method
		self.url = url
		self.parameter = parameter
		self.header = header
		self.qs = qs
		self.body = body
		self.onRequest = onRequest
		self.onResponse = onResponse
		self.cors = cors
		self.description = description
		return
	
	def __call__(self, obj: Union[RequestRunner,RequestStreamRunner,RequestServerSentEventsRunner,RequestWebSocketRunner]):
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
				onRequest=self.onRequest,
				onResponse=self.onResponse,
				cors=self.cors
			), description=self.description)
			return
		if issubclass(obj, RequestStreamRunner):
			router.add(RouteRequestStream(
				obj=obj,
				method=self.method,
				url=self.url,
				parameter=self.parameter,
				header=self.header,
				qs=self.qs,
				cors=self.cors
			), description=self.description)
			return
		if issubclass(obj, RequestServerSentEventsRunner):
			router.add(RouteRequestServerSentEvents(
				obj=obj,
				method=self.method,
				url=self.url,
				parameter=self.parameter,
				header=self.header,
				qs=self.qs,
				cors=self.cors
			), description=self.description)
			return
		if issubclass(obj, RequestWebSocketRunner):
			router.add(RouteRequestWebSocket(
				obj=obj,
				url=self.url,
				parameter=self.parameter,
				header=self.header,
				qs=self.qs,
				cors=self.cors,
			), description=self.description)
			return
		raise RuntimeError('{} is not support type'.format(obj.__name__))
