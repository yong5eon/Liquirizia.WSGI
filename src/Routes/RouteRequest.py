# -*- coding: utf-8 -*-

from ..Route import Route
from ..RouteRun import RouteRun

from ..Request import Request
from ..Properties import RequestRunner
from ..Filters import *
from ..RequestReader import RequestReader
from ..ResponseWriter import ResponseWriter
from ..Parser import Parser
from ..CORS import CORS
from ..Errors import BadRequestError, UnsupportedMediaTypeError

from Liquirizia.Validator import Validator

from collections.abc import Mapping, Sequence

from typing import Type, Dict

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
		content: Validator = None,
		contentParsers: Dict[str, Parser] = {},
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
		self.content = content
		self.contentParsers = {}
		for k, v in contentParsers.items() if contentParsers else {}: self.contentParsers[k.lower()] = v
		return

	def run(
		self,
		request: Request,
		reader: RequestReader,
		writer: ResponseWriter,
	):
		content = None
		if request.size:
			buffer = reader.read(request.size)
			if not buffer:
				raise BadRequestError('body is empty')
			content = buffer.decode(request.charset if request.charset else 'utf-8')
			if not request.format:
				raise BadRequestError('content-type header is required')
			if request.format.lower() not in self.contentParsers.keys():
				raise UnsupportedMediaTypeError('{} is not supported media type'.format(request.format))
			parse = self.contentParsers[request.format]
			try:
				content = parse(content)
			except Exception as e:
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
			request.args = self.qs(request.args)

		if self.content:
			content = self.content(content)

		if self.onRequest:
			request, response = self.onRequest(request)
			if response:
				writer.response(response)
				return

		obj = self.object(request)
		response = None
		if content:
			if isinstance(content, Mapping):
				response = obj.run(**content)
			elif not isinstance(content, (str, bytes)) and isinstance(content, Sequence):
				response = obj.run(*content)
			else:
				response = obj.run(content)
		else:
			response = obj.run()
		if not response:
			raise RuntimeError('{} must be return Response in run'.format(obj.__class__.__name__))

		if self.onResponse:
			response = self.onResponse(response)

		writer.response(response)
		return
