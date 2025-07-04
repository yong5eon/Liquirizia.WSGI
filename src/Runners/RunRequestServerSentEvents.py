# -*- coding: utf-8 -*-

from ..Route import Route
from ..RequestFactory import RequestFactory
from ..Request import Request
from ..Properties import (
	RequestServerSentEventsRunner,
	Origin,
	Auth,
	Parameters,
	QueryString,
	Headers,
)
from ..RequestReader import RequestReader
from ..ResponseWriter import ResponseWriter

from ..Extends import ServerSentEvents

from typing import Type

__all__ = (
	'RunRequestServerSentEvents'
)


class RunRequestServerSentEvents(Route, RequestFactory):
	"""Run Request Server Sent Events Class"""

	def __init__(
		self,
		obj: Type[RequestServerSentEventsRunner],
		method: str,
		url: str,
		origin: Origin = None,
		auth: Auth = None,
		parameters: Parameters = None,
		qs: QueryString = None,
		headers: Headers = None,
	):
		super().__init__(method, url)
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
		o.run(ServerSentEvents(writer))
		return
