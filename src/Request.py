# -*- coding: utf-8 -*-

from .Utils import ParseHeader

from urllib.parse import parse_qs, unquote, urlencode
from uuid import uuid4
from typing import Any, Optional, Dict, List

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

	def __repr__(self) -> str:
		return 'Request({})'.format({
			'address': self.address,
			'port': self.port,
			'protocol': self.scheme,
			'method': self.method,
			'uri': self.path,
			'querystring': self.args,
			'headers': self.props,
			'body': self.body,
		})

	def __str__(self) -> str:
		return '{} {}'.format(self.method, self.path)

	def header(self, key: str, value: Any = None) -> Optional[Any]:
		if value is not None:
			self.props[key] = value 
			return
		else:
			if key not in self.props.keys():
				return None
			return ParseHeader(key, str(self.props[key]))

	def headers(self) -> List:
		return [(key, value) for key, value in self.props.items()]
	
	@property
	def uri(self) -> str:
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
	def size(self) -> int:
		_ = self.header('Content-Length')
		if not _: return 0
		return _

	@property
	def format(self) -> Optional[str]:
		_ = self.header('Content-Type')
		if not _: return None
		return _.type

	@property
	def charset(self) -> Optional[str]:
		_ = self.header('Content-Type')
		if not _: return None
		return _.charset

	@property
	def qs(self) -> Dict:
		return self.args

	@qs.setter
	def qs(self, args):
		if not isinstance(args, dict):
			raise RuntimeError('querystring must be dict')
		self.args = args
		return

	@property
	def body(self) -> Optional[bytes]:
		return self.obj

	@body.setter
	def body(self, body):
		self.obj = body
		return
	
	@property
	def parameters(self) -> Optional[Dict]:
		return self.params

	@property
	def scheme(self) -> str:
		_ = self.header('X-Forwarded-Proto')
		if _: return _
		_ = self.header('Forwarded')
		if _:
			if 'Proto' in _[0]: return _[0]['Proto'].upper()
			if 'proto' in _[0]: return _[0]['proto'].upper()
		return 'HTTP'
	
	@property
	def protocol(self) -> str:
		return self.scheme

	@property
	def remote(self) -> str:
		_ = self.header('X-Real-IP')
		if _: return _
		_ = self.header('X-Forwarded-For')
		if _: return _
		_ = self.header('Forwarded')
		if _:
			if 'For' in _[0]: return _[0]['For']
			if 'for' in _[0]: return _[0]['for']
		return self.address

	@property
	def platform(self) -> str:
		return self.header('Sec-CH-UA-Platform')
	
	@property
	def device(self) -> str:
		return self.header('Sec-CH-UA-Model')
	
	@property
	def isMobile(self) -> bool:
		return self.header('Sec-CH-UA-Mobile')
