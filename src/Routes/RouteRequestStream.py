# -*- coding: utf-8 -*-

from ..Route import Route
from ..RouteRun import RouteRun

from ..Request import Request
from ..Properties import RequestStreamRunner
from ..Filters import *
from ..RequestReader import RequestReader
from ..ResponseWriter import ResponseWriter
from ..CORS import CORS

from Liquirizia.Validator import Validator

from typing import Type

__all__ = (
	'RouteRequestStream'
)


class RouteRequestStream(Route, RouteRun):
	"""Route Request Stream Class"""

	def __init__(
		self,
		obj: Type[RequestStreamRunner],
		method: str,
		url: str,
		parameter: Validator = None,
		header: Validator = None,
		qs: Validator = None,
		onRequest: RequestFilter = None,
		cors=CORS(),
	):
		super(RouteRequestStream, self).__init__(method, url, cors=cors)
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
		obj.run(reader, writer)
		return
	