# -*- coding: utf-8 -*-

from .Cookie import Cookie
from .Utils import ParseHeader

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
			'headers': self.props,
			'body': self.body,
		})

	def __str__(self):
		return '{} {}'.format(self.method, self.path)

	def header(self, key: str, value=None):
		key = key.replace('-','_').upper()
		if value is not None:
			self.props[key] = ParseHeader(key, str(value))
			return
		else:
			if key not in self.props.keys():
				return None
			return self.props[key]

	def headers(self):
		return [(key, value) for key, value in self.props.items()]
	
	@property
	def remoteAddress(self):
		_ = self.header('X-Real-IP')
		if _:
			return _
		_ = self.header('X-Forwarded-For')
		if _:
			return _[0]
		_ = self.header('Forwarded')
		if _:
			if 'For' in _[0]: return _[0]['For']
			if 'for' in _[0]: return _[0]['for']
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
		return self.header('Content-Length')

	@property
	def format(self):
		_ = self.header('Content-Type')
		if not _: return None
		return _.type

	@property
	def charset(self):
		_ = self.header('Content-Type')
		if not _: return None
		return _.charset

	@property
	def remote(self):
		_ = self.header('X-Real-IP')
		if _:
			return '{}({}):{}'.format(
				_,
				self.address,
				self.port,
			)
		_ = self.header('X-Forwarded-For')
		if _:
			return '{}({}):{}'.format(
				_,
				self.address,
				self.port,
			)
		_ = self.header('Forwarded')
		if _:
			if 'For' in _[0]:
				return '{}({}):{}'.format(
					_[0]['For'],
					self.address,
					self.port,
				)
			if 'for' in _[0]:
				return '{}({}):{}'.format(
					_[0]['for'],
					self.address,
					self.port,
				)
		return '{}:{}'.format(self.address, self.port)

	@property
	def scheme(self):
		_ = self.header('X-Forwarded-Proto')
		if _: return _
		_ = self.header('Forwarded')
		if _:
			if 'Proto' in _[0]: return _[0]['Proto']
			if 'proto' in _[0]: return _[0]['proto']
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
