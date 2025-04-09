# -*- coding: utf-8 -*-

from .Request import Request
from .Router import Router
from .Routes import (
	RouteOptions,
	RouteFile,
	RouteFileSystemObject,
	RouteRequest,
	RouteRequestStream,
	RouteRequestWebSocket,
	RouteRequestServerSentEvents,
)
from .Properties import (
	RequestRunner,
	RequestStreamRunner,
	RequestWebSocketRunner,
	RequestServerSentEventsRunner,
)
from .Properties.Validator import (
	Origin,
	Auth,
	Parameter,
	QueryString,
	Header,
	Body,
)
from .Filters import (
	RequestFilter,
	ResponseFilter,
)
from Liquirizia.FileSystemObject import Connection
from .Request import Request
from .RequestReader import RequestReader
from .ResponseWriter import ResponseWriter
from .Error import Error
from .Errors import (
	InternalServerError,
	ServiceUnavailableError,
	MethodNotAllowedError,
	NotFoundError,
)
from .Responses import ResponseError
from .Description import Response
from .Utils import ToHeader

from .Handler import Handler

from platform import system
from os import walk
from os.path import splitext
from uuid import uuid4

from typing import Type, Dict, Callable, Sequence, Union

__all__ = (
	'Application'
)


class Application(object):
	"""WSGI Application Class"""
	def __init__(
		self, 
		headers: Dict[str, str] = None,
		handler: Handler = None,
	):
		self.router = Router()
		self.headers = headers if headers else {}
		self.requestHandler = handler
		return

	def __call__(self, env: Dict, send: Callable):
		try:
			env['PATH_INFO'] = env['PATH_INFO'].encode('latin1').decode('utf-8')
			env['REQUEST_ID'] = uuid4().hex

			request = None
			runner = None
			parameters = None
			headers = {}

			for k, v in env.items():
				if k[0:5] == 'HTTP_':
					k = ToHeader(k[5:])
					k = self.toHeaderName(k)
					headers[k] = v
					continue
				if k in ['CONTENT_TYPE', 'CONTENT_LENGTH'] and v:
					k = ToHeader(k)
					k = self.toHeaderName(k)
					headers[k] = v
					continue

			if env['REQUEST_METHOD'] == 'OPTIONS':
				runner = RouteOptions()
			else:
				_, patterns = self.router.matches(env['PATH_INFO'])
				if not _ or not patterns:
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
			writer = ResponseWriter(request, send, self.requestHandler)
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
				write = send(str(response), response.headers())
				write(response.body if response.body else b'')
			except Exception as e:
				if self.requestHandler:
					response = self.requestHandler.onRequestException(request, e)
				else:
					response = ResponseError(InternalServerError(str(e), error=e))
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
	
	def toHeaderName(self, key) -> str:
		if not self.headers:
			return key
		if not isinstance(self.headers, dict):
			return key
		return self.headers.get(key, key)
	
	def addFile(
		self,
		path,
		url,
		onRequest: RequestFilter = None,
		onResponse: ResponseFilter = None,
	):
		self.router.add(RouteFile(
			url,
			path,
			onRequest=onRequest,
			onResponse=onResponse,
		))
		return

	def addFiles(
		self,
		path,
		prefix,
		onRequest: RequestFilter = None,
		onResponse: ResponseFilter = None,
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
				))
		return

	def addFileSystemObject(
		self,
		fso: Connection,
		prefix,
		onRequest: RequestFilter = None,
		onResponse: ResponseFilter = None,
	):
		self.router.add(RouteFileSystemObject(
			fso=fso,
			prefix=prefix,
			onRequest=onRequest,
			onResponse=onResponse,
		))
		return

	def add(
		self,
		object: Type[RequestRunner],
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
		self.router.add(RouteRequest(
			obj=object,
			method=method,
			url=url,
			origin=origin,
			auth=auth,
			parameter=parameter,
			qs=qs,
			header=header,
			body=body,
			response=response,
			onRequest=onRequest,
			onResponse=onResponse,
		))
		return

	def addStream(
		self,
		object: Type[RequestStreamRunner],
		method: str,
		url: str,
		origin: Origin = None,
		auth: Auth = None,
		parameter: Parameter = None,
		qs: QueryString = None,
		header: Header = None,
	):
		self.router.add(RouteRequestStream(
			obj=object,
			method=method,
			url=url,
			origin=origin,
			auth=auth,
			parameter=parameter,
			qs=qs,
			header=header,
		))
		return

	def addWebSocket(
		self,
		object: Type[RequestWebSocketRunner],
		url: str,
		origin: Origin = None,
		auth: Auth = None,
		parameter: Parameter = None,
		qs: QueryString = None,
		header: Header = None,
	):
		self.router.add(RouteRequestWebSocket(
			obj=object,
			url=url,
			origin=origin,
			auth=auth,
			parameter=parameter,
			qs=qs,
			header=header,
		))
		return

	def addServerSentEvents(
		self,
		object: Type[RequestServerSentEventsRunner],
		url: str,
		origin: Origin = None,
		auth: Auth = None,
		parameter: Parameter = None,
		qs: QueryString = None,
		header: Header = None,
	):
		self.router.add(RouteRequestServerSentEvents(
			obj=object,
			url=url,
			origin=origin,
			auth=auth,
			parameter=parameter,
			qs=qs,
			header=header,
		))
		return
