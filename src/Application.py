# -*- coding: utf-8 -*-

from .Configuration import Configuration

from .Request import Request
from .Router import Router
from .Routes import (
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

from .Responses import (
	ResponseError,
	ResponseOK,
	ResponseNoContent,
)
from .Errors import (
	InternalServerError,
	ServiceUnavailableError,
	MethodNotAllowedError,
	NotFoundError,
)
from .Util import ToHeaderName

from .Handler import Handler

from platform import system
from os import walk
from os.path import splitext, split
from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib import import_module
from pkgutil import walk_packages
from copy import copy

from typing import Type, Dict, Callable

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
			request = None
			headers = {}
			for k, v in env.items():
				if k[0:5] == 'HTTP_':
					k=ToHeaderName(k[5:])
					k=self.config.toHeaderName(k)
					headers[k] = v
				if k in ['CONTENT_TYPE', 'CONTENT_LENGTH'] and v:
					headers[ToHeaderName(k)] = v

			if env['REQUEST_METHOD'] == 'OPTIONS' and env['PATH_INFO'] == '*': 
				response = ResponseNoContent()
				# TODO : get methods from router
				response.header('Allow', ', '.join(sorted(list(set(self.router.methods)))))
				write = send(str(response), headers=response.headers())
				write(response.body if response.body else b'')
				return

			patterns = self.router.matches(env['PATH_INFO'])

			if not patterns:
				raise NotFoundError('{} is not found in router'.format(env['PATH_INFO']))

			if env['REQUEST_METHOD'] == 'OPTIONS':
				# TODO : if Access-Control-Request-Method in headers, response specific CORS headers
				# TODO : Use ResponseOK in HTTP/1.0
				response = ResponseNoContent()
				response.header('Allow', ', '.join(patterns.keys()))
				response.header('Access-Control-Allow-Methods', ', '.join(patterns.keys()))
				cors = CORS(
					origin=self.config.cors.origin,
					headers=self.config.cors.headers,
					exposeHeaders=self.config.cors.exposeHeaders,
					credentials=self.config.cors.credentials,
					age=self.config.cors.age,
				)
				for _, match in patterns.items():
					if match.route.cors.origin: cors.origin.extend(match.route.cors.origin)
					if match.route.cors.headers: cors.headers.extend(match.route.cors.headers)
					if match.route.cors.credentials: cors.credentials = match.route.cors.credentials
					if match.route.cors.exposeHeaders: cors.exposeHeaders.extend(match.route.cors.exposeHeaders)
					if match.route.cors.age and match.route.cors.age > cors.age: cors.age = match.route.cors.age
				for k, v in cors.toHeaders().items(): response.header(k, v)
				write = send(str(response), headers=response.headers())
				write(response.body if response.body else b'')
				return

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
			)
			cors = CORS(
				origin=self.config.cors.origin,
				headers=self.config.cors.headers,
				exposeHeaders=self.config.cors.exposeHeaders,
				credentials=self.config.cors.credentials,
				age=self.config.cors.age,
			)
			if runner.cors:
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
					response = ResponseError(e)
				for k, v in cors.toHeaders().items(): response.header(k, v)
				write = send(str(response), response.headers())
				write(response.body if response.body else b'')
		except Error as e:
			if self.requestHandler: 
				response = self.requestHandler.onError(e)
			else:
				response = ResponseError(e)
			cors = CORS(
				origin=self.config.cors.origin,
				headers=self.config.cors.headers,
				exposeHeaders=self.config.cors.exposeHeaders,
				credentials=self.config.cors.credentials,
				age=self.config.cors.age,
			)
			for k, v in cors.toHeaders().items(): response.header(k, v)
			write = send(str(response), response.headers())
			write(response.body if response.body else b'')
		except Exception as e:
			if self.requestHandler: 
				response = self.requestHandler.onException(e)
			else:
				response = ResponseError(ServiceUnavailableError(e))
			cors = CORS(
				origin=self.config.cors.origin,
				headers=self.config.cors.headers,
				exposeHeaders=self.config.cors.exposeHeaders,
				credentials=self.config.cors.credentials,
				age=self.config.cors.age,
			)
			for k, v in cors.toHeaders().items(): response.header(k, v)
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
		body: Validator = None,
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
			body=body,
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

	def load(self, mod: str = None, path: str = None, ext: str = 'py'):
		if mod:
			self.loadModule(mod)
		if path:
			ps = Path(path).rglob('*.{}'.format(ext))
			for p in ps if ps else []:
				p = self.loadPath(str(p))
		return
	
	def loadPath(self, path):
		head, tail = split(path)
		file, ext = splitext(tail)
		head = head.replace('\\', '.').replace('/', '.')
		mod = '{}.{}'.format(head, file)
		loader = SourceFileLoader(mod, path)
		mo = loader.load_module()
		if not mo:
			return None
		return mo
	
	def loadModule(self, mod):
		pkg = import_module(mod)
		for _, name, isPackage in walk_packages(pkg.__path__):
			fullname = pkg.__name__ + '.' + name
			if isPackage:
				self.loadModule(fullname)
				continue
			import_module(fullname)
		return
