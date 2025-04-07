# -*- coding: utf-8 -*-

from ..Route import Route
from ..RequestFactory import RequestFactory

from ..Request import Request
from ..Properties import  RequestServerSentEventsRunner
from ..Validator import (
	Origin,
	Auth,
	Parameter,
	QueryString,
	Header,
)
from ..Filters import *
from ..RequestReader import RequestReader
from ..ResponseWriter import ResponseWriter

from ..Extends import ServerSentEvents

from typing import Type

__all__ = (
	'RouteRequestServerSentEvents'
)


class RouteRequestServerSentEvents(Route, RequestFactory):
	"""Route Request Stream Chunked Class"""

	def __init__(
		self,
		obj: Type[RequestServerSentEventsRunner],
		method: str,
		url: str,
		origin: Origin = None,
		auth: Auth = None,
		parameter: Parameter = None,
		qs: QueryString = None,
		header: Header = None,
	):
		super(RouteRequestServerSentEvents, self).__init__(method, url)
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
		o.run(ServerSentEvents(writer))
		return
