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
from .Response import Response
from .ResponseWriter import ResponseWriter
from .Error import Error

from .Responses import (
	ResponseError,
	ResponseOK,
)
from .Errors import (
	InternalServerError,
	MethodNotAllowedError,
	NotFoundError,
)
from .Util import ToHeaderName

from .RequestHandler import RequestHandler

from platform import system
from os import walk
from os.path import splitext, split
from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib import import_module
from pkgutil import walk_packages

from typing import Type

__all__ = (
	'Application'
)


class Application(object):
	"""WSGI Application Class"""

	def __init__(
		self, 
		conf: Configuration = Configuration(),
		handler: RequestHandler = None,
		onRequest: RequestFilter = None,
	):
		self.router = Router()
		self.config = conf
		self.requestHandler = handler
		self.onRequest = onRequest
		return

	def __call__(self, env: dict, send):
		try:
			request = None
			headers = {}
			for k, v in env.items():
				if k[0:5] == 'HTTP_':
					k=ToHeaderName(k[5:])
					k=self.config.toHeaderName(k)
					headers[k] = v
				if k in ['CONTENT_TYPE', 'CONTENT_LENGTH']:
					headers[ToHeaderName(k)] = v

			patterns = self.router.matches(env['PATH_INFO'])
			if not patterns:
				raise NotFoundError('{} is not found in router'.format(env['PATH_INFO']))
	
			if env['REQUEST_METHOD'] == 'OPTIONS':
				if 'Access-Control-Request-Method' in headers:
					response = ResponseOK(
						body=', '.join(patterns.keys()),
						format='text/plain',
						charset='utf-8',
					)
					# response.header('Access-Control-Allow-Methods', ', '.join(patterns.keys()))
					response.header('Allow', ', '.join(patterns.keys()))
					send(str(response), headers=response.headers())
					yield response.body if response.body else b''

				route = patterns[headers['Access-Control-Request-Method']].route
				cors = route.headers()
		
				response = ResponseOK()
				for key, value in cors.items():
					response.header(key, value)
				send(str(response), response.headers())
				yield response.body if response.body else b''
	
			if env['REQUEST_METHOD'] not in patterns.keys():
				raise MethodNotAllowedError('{} is not allowed for {}'.format(
					env['REQUEST_METHOD'],
					env['PATH_INFO']
				))
	
			runner = patterns[env['REQUEST_METHOD']].route
			parameters = patterns[env['REQUEST_METHOD']].params

			reader = RequestReader(env['wsgi.input'])
			writer = ResponseWriter(send, self.requestHandler.onResponse)
			request = Request(
				address=env['REMOTE_ADDR'],
				port=env['REMOTE_PORT'] if 'REMOTE_PORT' in env else 0,
				method=env['REQUEST_METHOD'],
				uri='{}{}'.format(
					env['PATH_INFO'],
					'?{}'.format(env['QUERY_STRING']) if 'QUERY_STRING' in env and env['QUERY_STRING'] else ''
				),
				parameters=parameters,
				headers=headers,
			)
			if self.requestHandler: 
				request, response = self.requestHandler.onRequest(request)
				if response:
					send(str(response), response.headers())
					yield response.body if response.body else b''
			if self.onRequest:
				request, response = self.onRequest(request)
				if response:
					send(str(response), response.headers())
					yield response.body if response.body else b''
			runner.run(request, reader, writer)
			if self.requestHandler:
				self.requestHandler.onRequestComplete(request)
		except Error as e:
			if self.requestHandler: 
				if not request:
					request = Request(
						address=env['REMOTE_ADDR'],
						port=env['REMOTE_PORT'] if 'REMOTE_PORT' in env else 0,
						method=env['REQUEST_METHOD'],
						uri='{}{}'.format(
							env['PATH_INFO'],
							'?{}'.format(env['QUERY_STRING']) if 'QUERY_STRING' in env and env['QUERY_STRING'] else ''
						),
						parameters={},
						headers=headers,
					)
				response = self.requestHandler.onError(request, e)
			else:
				response = ResponseError(e)
			send(str(response), response.headers())
			yield response.body if response.body else b''
		except BaseException as e:
			if self.requestHandler: 
				response = self.requestHandler.onException(request, e)
			else:
				response = ResponseError(InternalServerError(e))
			send(str(response), response.headers())
			yield response.body if response.body else b''
	
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
			onResponse=onResponse
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
					onResponse=onResponse
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
			onResponse=onResponse
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
		cors: CORS = None,
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
			cors=cors
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
		cors: CORS = None,
	):
		self.router.add(RouteRequestStream(
			obj=object,
			method=method,
			url=url,
			parameter=parameter,
			header=header,
			qs=qs,
			cors=cors
		))
		return

	def addWebSocket(
		self,
		object: Type[RequestWebSocketRunner],
		url: str,
		qs: Validator = None,
		cors: CORS = None,
	):
		self.router.add(RouteRequestWebSocket(
			obj=object,
			url=url,
			qs=qs,
			cors=cors
		))
		return
	
	def addServerSentEvents(
		self,
		object: Type[RequestServerSentEventsRunner],
		url: str,
		parameter: Validator = None,
		header: Validator = None,
		qs: Validator = None,
		cors: CORS = None,
	):
		self.router.add(RouteRequestServerSentEvents(
			obj=object,
			url=url,
			parameter=parameter,
			header=header,
			qs=qs,
			cors=cors
		))


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
