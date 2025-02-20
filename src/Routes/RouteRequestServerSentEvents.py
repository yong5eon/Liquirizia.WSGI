# -*- coding: utf-8 -*-

from ..Route import Route
from ..RouteRun import RouteRun

from ..Request import Request
from ..Properties import RequestServerSentEventsRunner
from ..Filters import *
from ..RequestReader import RequestReader
from ..ResponseWriter import ResponseWriter
from ..CORS import CORS

from Liquirizia.Validator import Validator

from ..Extends import ServerSentEvents

from typing import Type

__all__ = (
	'RouteRequestServerSentEvents'
)


class RouteRequestServerSentEvents(Route, RouteRun):
	"""Route Request Stream Chunked Class"""

	def __init__(
		self,
		obj: Type[RequestServerSentEventsRunner],
		method: str,
		url: str,
		parameter: Validator = None,
		header: Validator = None,
		qs: Validator = None,
		cors=CORS(),
	):
		super(RouteRequestServerSentEvents, self).__init__(method, url, cors=cors)
		self.object = obj
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

		obj = self.object(request)
		obj.run(ServerSentEvents(writer))
		return
	