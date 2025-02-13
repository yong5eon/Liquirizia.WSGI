# -*- coding: utf-8 -*-

from ..Route import Route
from ..RouteRun import RouteRun

from ..Request import Request
from ..Filters import *
from ..RequestReader import RequestReader
from ..ResponseWriter import ResponseWriter
from ..CORS import CORS

from ..Responses import (
	ResponseBuffer,
	ResponseNotModified,
	ResponseNotFound,
)
from ..Utils import DateToTimestamp

from Liquirizia.FileSystemObject import Connection
from datetime import timezone
from re import compile

__all__ = (
	'RouteFileSystemObject'
)


class RouteFileSystemObject(Route, RouteRun):
	"""File System Object Route Class"""

	def __init__(
		self,
		prefix: str,
		fso: Connection,
		onRequest: RequestFilter = None,
		onResponse: ResponseFilter = None,
		cors: CORS = CORS(),
	):
		super(RouteFileSystemObject, self).__init__('GET', '{}'.format(prefix), cors=cors)
		self.prefix = prefix
		self.fso = fso
		self.regex = compile('^{}/'.format(prefix))
		self.onRequest = onRequest
		self.onResponse = onResponse
		return

	def match(self, url: str):
		m = self.regex.match(url)
		if not m:
			return False, None
		return True, {
			'path': url[len(self.prefix)+1:]
		}

	def run(
		self,
		request: Request,
		reader: RequestReader,
		writer: ResponseWriter,
	):
		if self.onRequest:
			request, response = self.onRequest(request)
			if response:
				writer.response(response)
				return

		m, parameters = self.match(request.uri)

		if request.header('ETag') and request.header('ETag') == self.fso.etag(parameters['path']):
			response = ResponseNotModified()
			for k, v in self.headers(request).items():
				response.header(k, v)
			writer.response(response)
			return

		if request.header('If-Modified-Since'):
			timestamp = request.header('If-Modified-Since').replace(tzinfo=timezone.utc).timestamp()
			if timestamp and timestamp >= self.fso.timestamp(parameters['path']):
				response = ResponseNotModified()
				for k, v in self.headers(request).items():
					response.header(k, v)
				writer.response(response)
				return 

		# TODO : use cache instead of origin

		m, parameters = self.match(request.uri)

		f = self.fso.open(parameters['path'], mode='rb')

		if not f:
			response = ResponseNotFound()
			writer.send(response, headers=self.headers(request))
			return

		format, charset = self.fso.type(parameters['path'])

		if request.header('Range'):
			# TODO : seek to range
			pass
		buffer = f.read()

		response = ResponseBuffer(buffer, len(buffer), format=format, charset=charset)

		if self.onResponse:
			response = self.onResponse.run(response)

		writer.response(response)
		return
