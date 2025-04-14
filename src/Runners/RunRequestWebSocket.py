# -*- coding: utf-8 -*-

from ..Route import Route
from ..RequestFactory import RequestFactory
from ..Request import Request
from ..Properties import RequestWebSocketRunner
from ..Validators import (
	Origin,
	Auth,
	Parameter,
	QueryString,
	Header,
	Body,
)
from ..Filters import *
from ..RequestReader import RequestReader
from ..ResponseWriter import ResponseWriter
from ..Extends import WebSocket

from ..Errors import (
	NotAcceptableError,
)

from Liquirizia.Validator import Validator

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
		parameter: Parameter = None,
		qs: QueryString = None,
		header: Header = None,
	):
		super().__init__('GET', url)
		self.object = obj
		self.origin = origin
		self.auth = auth
		self.parameter = parameter
		self.qs = qs
		self.header = header
		return

	def run(
		self,
		request: Request,
		reader: RequestReader,
		writer: ResponseWriter,
	):
		if self.origin: self.origin(request)
		if self.auth: self.auth(request)
		if self.parameter: self.parameter(request)
		if self.qs: self.qs(request)
		if self.header: self.header(request)

		o = self.object(request)
		if request.header('Sec-WebSocket-Protocol') and not o.switch(request.header('Sec-WebSocket-Protocol')):
				raise NotAcceptableError(reason='{} is not acceptable protocol'.format(request.header('Sec-WebSocket-Protocol')))
		ws = WebSocket(reader, writer)
		ws.switch(request.header('Sec-WebSocket-Key'), protocol=request.header('Sec-WebSocket-Protocol'))
		ws.run(o.run)
		ws.end()
		return
