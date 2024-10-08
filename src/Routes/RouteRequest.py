# -*- coding: utf-8 -*-

from ..Route import Route
from ..RouteRun import RouteRun

from ..Request import Request
from ..Properties import RequestRunner
from ..Filters import *
from ..RequestReader import RequestReader
from ..ResponseWriter import ResponseWriter
from ..CORS import CORS
from ..Errors import BadRequestError, UnsupportedMediaTypeError

from Liquirizia.Serializer import SerializerHelper
from Liquirizia.Serializer.Errors import NotSupportedError, DecodeError
from Liquirizia.Validator import Validator

from typing import Type

__all__ = (
	'RouteRequest'
)


class RouteRequest(Route, RouteRun):
	"""Route Request Class"""

	def __init__(
		self,
		obj: Type[RequestRunner],
		method: str,
		url: str,
		parameter: Validator = None,
		header: Validator = None,
		qs: Validator = None,
		body: Validator = None,
		onRequest: RequestFilter = None,
		onResponse: ResponseFilter = None,
		cors=CORS(),
	):
		super(RouteRequest, self).__init__(method, url, cors=cors)
		self.object = obj
		self.onRequest = onRequest
		self.onResponse = onResponse
		self.header = header
		self.parameter = parameter
		self.qs = qs
		self.body = body
		return

	def run(
		self,
		request: Request,
		reader: RequestReader,
		writer: ResponseWriter,
	):
		if request.size:
			try:
				request.body = SerializerHelper.Decode(
					reader.read(request.size),
					format=request.format,
					charset=request.charset,
				)
			except NotSupportedError as e:
				raise UnsupportedMediaTypeError(str(e), error=e)
			except DecodeError as e:
				raise BadRequestError(str(e), error=e)

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
			request.qs = self.qs(request.qs)

		if self.body:
			request.body = self.body(request.body)


		if self.onRequest:
			request, response = self.onRequest.run(request)
			if response:
				writer.response(response)
				return

		obj = self.object(request)
		response = obj.run()

		if self.onResponse:
			response = self.onResponse.run(response)

		writer.response(response)
		return
