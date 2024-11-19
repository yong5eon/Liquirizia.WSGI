# -*- coding: utf-8 -*-

from .Cookie import Cookie
from .Util import ToHeaderName, ParseHeader

from http.cookies import SimpleCookie
from urllib.parse import parse_qs, unquote, urlencode

from uuid import uuid4

__all__ = (
	'Request'
)


class Request(object):
	"""HTTP Request Class for WSGI"""

	def __init__(
		self, 
		address: str,
		port: int,
		method: str, 
		uri: str, 
		parameters: dict,
		headers: dict = None, 
		body: bytes = None, 
		format: str = None, 
		charset: str = None,
		id: str = None,
	):
		self.id = id if id else uuid4().hex
		self.address = address
		self.port = port
		self.method = method
		self.params = parameters
		self.path, *querystring = uri.split('?', 1)
		querystring = querystring[0] if len(querystring) else None
		self.args = parse_qs(unquote(querystring), keep_blank_values=True) if querystring else {}
		for k, v in self.args.items():
			if len(v) == 0:
				self.args[k] = None
			elif len(v) == 1:
				self.args[k] = v[0] if len(v[0]) else None
			else:
				for i, o in enumerate(v):
					v[i] = o if len(o) else None
				self.args[k] = v
		self.props = {}
		self.cookies = {}
		for k, v in headers.items() if headers else []:
			self.header(k, v)
		if body:
			self.header(
				'Content-Type',
				'{}{}'.format(
					format if format else 'application/octet-stream',
					'; charset={}'.format(charset) if charset else ''
				)
			)
		self.obj = body
		self.session = None
		return

	def __repr__(self):
		return 'Request({})'.format({
			'remoteAddress': self.address,
			'remotePort': self.port,
			'method': self.method,
			'uri': self.path,
			'queryString': self.args,
			'version': self.version,
			'headers': self.props,
			'cookies': self.cookies,
			'body': self.body,
		})

	def __str__(self):
		return '{} {}'.format(self.method, self.path)

	def header(self, key: str, value=None):
		if value is not None:
			if key == 'Cookie':
				c = SimpleCookie()
				c.load(value)
				for k, v in c.items():
					self.cookies[k] = Cookie(
						name=k,
						value=v.value,
						expires=v['expires'],
						path=v['path'],
						domain=v['domain'],
						secure=v['secure'],
						http=v['httponly'],
						version=v['version'],
						max=v['max-age'],
						comment=v['comment']
					)
			else:
				# TODO : according to value, use other parse methods. User-Agent, Accept-Language, ...
				self.props[key] = ParseHeader(str(value))
				return
		else:
			if key not in self.props.keys():
				return None
			return self.props[key]['expr']

	def headers(self):
		headers = [(key, value['expr']) for key, value in self.props.items()]

		cookies = SimpleCookie()

		for name, cookie in self.cookies.items():
			cookies[name] = cookie.value
			if cookie.expires:
				cookies[name]['expires'] = cookie.expires
			if cookie.path:
				cookies[name]['path'] = cookie.path
			if cookie.domain:
				cookies[name]['domain'] = cookie.domain
			if cookie.secure:
				cookies[name]['secure'] = cookie.secure
			if cookie.http:
				cookies[name]['httponly'] = cookie.http
			if cookie.version:
				cookies[name]['version'] = cookie.version
			if cookie.max:
				cookies[name]['max-age'] = cookie.max
			if cookie.comment:
				cookies[name]['comment'] = cookie.comment

		for name, cookie in cookies.items():
			headers.append(('Cookie', cookie.OutputString()))

		return headers
	
	@property
	def remoteAddress(self):
		if 'X-Forwarded-For' in self.props.keys():
			return self.props['X-Forwarded-For']['args'][0][0]
		if 'X-Real-IP' in self.props.keys():
			return self.props['X-Real-IP']['args'][0][0]
		return self.address
	
	@property
	def remotePort(self):
		return self.port

	@property
	def uri(self):
		return '{}{}'.format(
			self.path,
			'?{}'.format(self.querystring) if self.querystring and len(self.querystring) else '',
		)

	@property
	def querystring(self):
		if self.args and len(self.args.items()):
			return urlencode(self.args)
		return None

	@property
	def size(self):
		if 'Content-Length' not in self.props.keys():
			return 0
		return int(self.props['Content-Length']['expr'])

	@property
	def format(self):
		if 'Content-Type' not in self.props.keys():
			return None
		return self.props['Content-Type']['args'][0][0]

	@property
	def charset(self):
		if 'Content-Type' not in self.props.keys():
			return None
		if not self.props['Content-Type']['args'][0][1]:
			return None
		keys = {}
		for key in self.props['Content-Type']['args'][0][1].keys():
			keys[key.lower()] = key
		if 'charset' not in keys.keys():
			return None
		return self.props['Content-Type']['args'][0][1][keys['charset']][0]

	@property
	def remote(self):
		if 'X-Forwarded-For' in self.props.keys():
			return '{}({}):{}'.format(
				self.props['X-Forwarded-For']['args'][0][0],
				self.address,
				self.port,
			)
		if 'X-Real-IP' in self.props.keys():
			return '{}({}):{}'.format(
				self.props['X-Real-IP']['args'][0][0],
				self.address,
				self.port,
			)
		return '{}:{}'.format(self.address, self.port)

	@property
	def scheme(self):
		if 'X-Forwarded-Proto' in self.props.keys():
			return self.props['X-Forwarded-Proto']['expr']
		return 'HTTP'

	@property
	def qs(self):
		return self.args

	@qs.setter
	def qs(self, args):
		if not isinstance(args, dict):
			raise RuntimeError('querystring must be dict')
		self.args = args
		return

	@property
	def body(self):
		return self.obj

	@body.setter
	def body(self, body):
		self.obj = body
		return
	
	@property
	def parameters(self):
		return self.params
