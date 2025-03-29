# -*- coding: utf-8 -*-

from ..Route import Route
from ..RouteRun import RouteRun

from ..Request import Request
from ..Properties import RequestWebSocketRunner
from ..Filters import *
from ..RequestReader import RequestReader
from ..ResponseWriter import ResponseWriter
from ..CORS import CORS
from ..Extends import WebSocket

from ..Errors import (
	NotAcceptableError,
)

from Liquirizia.Validator import Validator

from typing import Type

__all__ = (
	'RouteRequestWebSocket'
)


class RouteRequestWebSocket(Route, RouteRun):
	"""Route Request WebSocket Class"""

	def __init__(
		self,
		obj: Type[RequestWebSocketRunner],
		url: str,
		parameter: Validator = None,
		header: Validator = None,
		qs: Validator = None,
		onRequest: RequestFilter = None,
		cors=CORS(),
	):
		super(RouteRequestWebSocket, self).__init__('GET', url, cors=cors)
		self.object = obj
		self.onRequest = onRequest
		self.parameter = parameter
		self.header = header
		self.qs = qs
		return

	def run(
		self,
		request: Request,
		reader: RequestReader,
		writer: ResponseWriter,
	):
		if self.parameter:
			request.params = self.parameter(request.params)

		if self.header:
			headers = {}
			for k, v in request.headers():
				headers[k] = v
			headers = self.header(headers)
			for k, v in headers.items():
				request.header(k, v)

		if self.qs:
			request.args = self.qs(request.args)

		if self.onRequest:
			request, response = self.onRequest(request)
			if response:
				writer.response(response)
				return

		obj = self.object(request)
		if request.header('Sec-WebSocket-Protocol') and not obj.switch(request.header('Sec-WebSocket-Protocol')):
				raise NotAcceptableError(reason='{} is not acceptable protocol'.format(request.header('Sec-WebSocket-Protocol')))
		ws = WebSocket(reader, writer)
		ws.switch(request.header('Sec-WebSocket-Key'), protocol=request.header('Sec-WebSocket-Protocol'))
		ws.run(obj.run)
		ws.end()
		return
