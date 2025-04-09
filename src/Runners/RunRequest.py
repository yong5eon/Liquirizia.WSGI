# -*- coding: utf-8 -*-

from ..Route import Route
from ..RequestFactory import RequestFactory
from ..Request import Request
from ..Properties import RequestRunner
from ..Properties.Validator import (
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
from ..Errors import BadRequestError
from ..Description import Response

from collections.abc import Mapping, Sequence

from typing import Type, Sequence, Union

__all__ = (
	'RunRequest'
)


class RunRequest(Route, RequestFactory):
	"""Run Request Class"""
	def __init__(
		self,
		obj: Type[RequestRunner],
		method: str,
		url: str,
		origin: Origin = None,
		auth: Auth = None,
		parameter: Parameter = None,
		qs: QueryString = None,
		header: Header = None,
		body: Body = None,
		response: Union[Response, Sequence[Response]] = None,
		onRequest: RequestFilter = None,
		onResponse: ResponseFilter = None,
	):
		super().__init__(method, url)
		self.object = obj
		self.origin = origin
		self.auth = auth
		self.parameter = parameter
		self.qs = qs
		self.header = header
		self.body = body
		self.response = response
		self.onRequest = onRequest
		self.onResponse = onResponse
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

		content = None
		if request.size:
			content = reader.read(request.size)
			if not content: raise BadRequestError('body is empty')

		if self.body: content = self.body(request, content)

		if self.onRequest:
			request, response = self.onRequest(request)
			if response:
				writer.response(response)
				return

		o = self.object(request)

		response = None
		if content:
			if isinstance(content, Mapping):
				response = o.run(**content)
			elif not isinstance(content, (str, bytes)) and isinstance(content, Sequence):
				response = o.run(*content)
			else:
				response = o.run(content)
		else:
			response = o.run()
		if not response:
			raise RuntimeError('{} must be return Response in run'.format(o.__class__.__name__))

		if self.onResponse:
			response = self.onResponse(response)

		# set CORS headers
		headers = []
		for k, v in response.headers():
			if k not in ['Set-Cookie', 'Content-Length']:
				headers.append(k)
		# set Access-Control-Allow-Origin, Vary
		# Access-Control-Allow-Origin: https://example.com
		# Vary: Origin
		if self.origin:
			origin = request.header('Origin')
			match = None
			for m in self.origin.matches:
				if origin == m:
					match = m
					break
			if match or self.origin.all:
				response.header('Access-Control-Allow-Origin', origin)
				response.header('Vary', 'Origin')
			# set Access-Control-Allow-Credentials if auth is not None
			# Access-Control-Allow-Credentials: true
			if self.auth and not self.origin.all:
				response.header('Access-Control-Allow-Credentials', 'true')
		# set Access-Control-Expose-Headers
		# Access-Control-Expose-Headers: X-Custom-Header, Content-Length
		if headers:
			response.header('Access-Control-Expose-Headers', ', '.join(headers))
		writer.response(response)
		return
