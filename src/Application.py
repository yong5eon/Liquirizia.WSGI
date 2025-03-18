# -*- coding: utf-8 -*-

from .Configuration import Configuration
from .Request import Request
from .Router import Router
from .RouteOptions import RouteOptions
from .Routes import (
	RouteFile,
	RouteFileSystemObject,
	RouteRequest,
	RouteRequestStream,
	RouteRequestWebSocket,
	RouteRequestServerSentEvents,
)
from .Decoder import Decoder
from .Decoders import (
	TextDecoder,
	FormUrlEncodedDecoder,
	JavaScriptObjectNotationDecoder,
)
from .Properties import (
	RequestRunner,
	RequestStreamRunner,
	RequestWebSocketRunner,
	RequestServerSentEventsRunner,
)
from .Filters import (
	RequestFilter,
	ResponseFilter,
)
from .CORS import CORS

from Liquirizia.Validator import Validator
from Liquirizia.FileSystemObject import Connection

from .Request import Request
from .RequestReader import RequestReader
from .ResponseWriter import ResponseWriter
from .Error import Error

from .Responses import ResponseError
from .Errors import (
	InternalServerError,
	ServiceUnavailableError,
	MethodNotAllowedError,
	NotFoundError,
)
from .Utils import ToHeader

from .Handler import Handler

from urllib.parse import unquote
from platform import system
from os import walk
from os.path import splitext
from uuid import uuid4

from typing import Type, Dict, Callable, Sequence

__all__ = (
	'Application'
)


class Application(object):
	"""WSGI Application Class"""

	def __init__(
		self, 
		conf: Configuration = Configuration(),
		handler: Handler = None,
	):
		self.router = Router()
		self.config = conf
		self.requestHandler = handler
		return

	def __call__(self, env: Dict, send: Callable):
		try:
			env['PATH_INFO'] = unquote(env['RAW_URI'].split('?')[0])
			env['REQUEST_ID'] = uuid4().hex

			request = None
			runner = None
			parameters = None
			headers = {}

			for k, v in env.items():
				if k[0:5] == 'HTTP_':
					k = ToHeader(k[5:])
					k = self.config.toHeaderName(k)
					headers[k] = v
					continue
				if k in ['CONTENT_TYPE', 'CONTENT_LENGTH'] and v:
					k = ToHeader(k)
					k = self.config.toHeaderName(k)
					headers[k] = v
					continue

			if env['REQUEST_METHOD'] == 'OPTIONS':
				runner = RouteOptions()
			else:
				patterns = self.router.matches(env['PATH_INFO'])
				if not patterns:
					raise NotFoundError('{} is not found in router'.format(env['PATH_INFO']))

				if env['REQUEST_METHOD'] not in patterns.keys():
					raise MethodNotAllowedError('{} is not allowed for {}'.format(
						env['REQUEST_METHOD'],
						env['PATH_INFO']
					))
				runner = patterns[env['REQUEST_METHOD']].route
				parameters = patterns[env['REQUEST_METHOD']].params

			reader = RequestReader(env['wsgi.input'])
			request = Request(
				address=env['REMOTE_ADDR'],
				port=env['REMOTE_PORT'] if 'REMOTE_PORT' in env.keys() else 0,
				method=env['REQUEST_METHOD'],
				uri='{}{}'.format(
					env['PATH_INFO'],
					'?{}'.format(env['QUERY_STRING']) if 'QUERY_STRING' in env and env['QUERY_STRING'] else ''
				),
				parameters=parameters,
				headers=headers,
				id=env['REQUEST_ID'],
			)
			cors = CORS(
				origin=self.config.cors.origin,
				headers=self.config.cors.headers,
				exposeHeaders=self.config.cors.exposeHeaders,
				credentials=self.config.cors.credentials,
				age=self.config.cors.age,
			)
			if hasattr(runner, 'cors') and getattr(runner, 'cors'):
				if runner.cors.origin: cors.origin.extend(runner.cors.origin)
				if runner.cors.headers: cors.headers.extend(runner.cors.headers)
				if runner.cors.credentials: cors.credentials = runner.cors.credentials
				if runner.cors.exposeHeaders: cors.exposeHeaders.extend(runner.cors.exposeHeaders)
				if runner.cors.age and runner.cors.age > cors.age : cors.age = runner.cors.age
			writer = ResponseWriter(
				request,
				send,
				self.requestHandler,
				cors,
			)
			try:
				if self.requestHandler: 
					request, response = self.requestHandler.onRequest(request)
					if response:
						write = send(str(response), response.headers())
						write(response.body if response.body else b'')
						return
				runner.run(request, reader, writer)
				if self.requestHandler:
					self.requestHandler.onRequestComplete(request)
			except Error as e:
				if self.requestHandler:
					response = self.requestHandler.onRequestError(request, e)
				else:
					response = ResponseError(e)
				for k, v in cors.toHeaders().items(): response.header(k, v)
				write = send(str(response), response.headers())
				write(response.body if response.body else b'')
			except Exception as e:
				if self.requestHandler:
					response = self.requestHandler.onRequestException(request, e)
				else:
					response = ResponseError(InternalServerError(str(e), error=e))
				for k, v in cors.toHeaders().items(): response.header(k, v)
				write = send(str(response), response.headers())
				write(response.body if response.body else b'')
		except Error as e:
			if self.requestHandler: 
				response = self.requestHandler.onError(env, e)
			else:
				response = ResponseError(e)
			write = send(str(response), response.headers())
			write(response.body if response.body else b'')
		except Exception as e:
			if self.requestHandler: 
				response = self.requestHandler.onException(env, e)
			else:
				response = ResponseError(ServiceUnavailableError(str(e), error=e))
			write = send(str(response), response.headers())
			write(response.body if response.body else b'')
		return
	
	def addFile(
		self,
		path,
		url,
		onRequest: RequestFilter = None,
		onResponse: ResponseFilter = None,
		cors: CORS = CORS(),
	):
		self.router.add(RouteFile(
			url,
			path,
			onRequest=onRequest,
			onResponse=onResponse,
			cors=cors,
		))
		return

	def addFiles(
		self,
		path,
		prefix,
		onRequest: RequestFilter = None,
		onResponse: ResponseFilter = None,
		cors: CORS = CORS(),
	):
		if system().upper() == 'WINDOWS':
			path = path.replace('/', '\\')
		else:
			path = path.replace('\\', '/')

		for (p, dir, files) in walk(path):
			for filename in files:
				ext = splitext(filename)[-1]
				file = ''
				if system().upper() == 'WINDOWS':
					file = '{}\\{}'.format(p, filename)
				else:
					file = '{}/{}'.format(p, filename)
				url = '{}{}'.format(prefix, file[len(path):].replace('\\', '/'))
				self.router.add(RouteFile(
					url=url,
					path=file,
					onRequest=onRequest,
					onResponse=onResponse,
					cors=cors,
				))
		return

	def addFileSystemObject(
		self,
		fso: Connection,
		prefix,
		onRequest: RequestFilter = None,
		onResponse: ResponseFilter = None,
		cors: CORS = CORS(),
	):
		self.router.add(RouteFileSystemObject(
			fso=fso,
			prefix=prefix,
			onRequest=onRequest,
			onResponse=onResponse,
			cors=cors,
		))
		return

	def add(
		self,
		object: Type[RequestRunner],
		method: str,
		url: str,
		parameter: Validator = None,
		header: Validator = None,
		qs: Validator = None,
		content: Validator = None,
		contentParsers: Sequence[Decoder] = (
			TextDecoder('utf-8'),
			FormUrlEncodedDecoder('utf-8'),
			JavaScriptObjectNotationDecoder('utf-8'),
		),
		onRequest: RequestFilter = None,
		onResponse: ResponseFilter = None,
		cors: CORS = CORS(),
	):
		self.router.add(RouteRequest(
			obj=object,
			method=method,
			url=url,
			parameter=parameter,
			header=header,
			qs=qs,
			content=content,
			contentParsers=contentParsers,
			onRequest=onRequest,
			onResponse=onResponse,
			cors=cors,
		))
		return

	def addStream(
		self,
		object: Type[RequestStreamRunner],
		method: str,
		url: str,
		parameter: Validator = None,
		header: Validator = None,
		qs: Validator = None,
		cors: CORS = CORS(),
	):
		self.router.add(RouteRequestStream(
			obj=object,
			method=method,
			url=url,
			parameter=parameter,
			header=header,
			qs=qs,
			cors=cors,
		))
		return

	def addWebSocket(
		self,
		object: Type[RequestWebSocketRunner],
		url: str,
		parameter: Validator = None,
		header: Validator = None,
		qs: Validator = None,
		cors: CORS = CORS(),
	):
		self.router.add(RouteRequestWebSocket(
			obj=object,
			url=url,
			parameter=parameter,
			header=header,
			qs=qs,
			cors=cors,
		))
		return

	def addServerSentEvents(
		self,
		object: Type[RequestServerSentEventsRunner],
		url: str,
		parameter: Validator = None,
		header: Validator = None,
		qs: Validator = None,
		cors: CORS = CORS(),
	):
		self.router.add(RouteRequestServerSentEvents(
			obj=object,
			url=url,
			parameter=parameter,
			header=header,
			qs=qs,
			cors=cors,
		))
		return
