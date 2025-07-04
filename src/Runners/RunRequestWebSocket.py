# -*- coding: utf-8 -*-

from ..Route import Route
from ..RequestFactory import RequestFactory
from ..Request import Request
from ..Properties import (
	RequestWebSocketRunner,
	Origin,
	Auth,
	Parameters,
	QueryString,
	Headers,
)
from ..RequestReader import RequestReader
from ..ResponseWriter import ResponseWriter
from ..Extends import WebSocket

from ..Errors import (
	NotAcceptableError,
)

from typing import Type

__all__ = (
	'RunRequestWebSocket'
)


class RunRequestWebSocket(Route, RequestFactory):
	"""Run Request WebSocket Class"""

	def __init__(
		self,
		obj: Type[RequestWebSocketRunner],
		url: str,
		origin: Origin = None,
		auth: Auth = None,
		parameters: Parameters = None,
		qs: QueryString = None,
		headers: Headers = None,
	):
		super().__init__('GET', url)
		self.object = obj
		self.origin = origin
		self.auth = auth
		self.parameters = parameters
		self.qs = qs
		self.headers = headers
		return

	def run(
		self,
		request: Request,
		reader: RequestReader,
		writer: ResponseWriter,
	):
		if self.origin: self.origin(request)
		if self.auth: self.auth(request)
		if self.parameters: self.parameters(request)
		if self.qs: self.qs(request)
		if self.headers: self.headers(request)

		o = self.object(request)
		if request.header('Sec-WebSocket-Protocol'):
			if not o.switch(request.header('Sec-WebSocket-Protocol')):
				raise NotAcceptableError(reason='{} is not acceptable protocol'.format(request.header('Sec-WebSocket-Protocol')))
		ws = WebSocket(reader, writer)
		ws.switch(request.header('Sec-WebSocket-Key'), protocol=request.header('Sec-WebSocket-Protocol'))
		ws.run(o.run)
		ws.end()
		return
