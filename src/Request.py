# -*- coding: utf-8 -*-

from .Utils import ParseHeader
from Liquirizia.Utils.Dictionary import CreateDataClass, ToDataClass

from urllib.parse import parse_qs, unquote, urlencode
from uuid import uuid4
from typing import Any, Optional, Dict, List, Union

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
		parameters: dict = None,
		headers: dict = None, 
		id: str = None,
	):
		self.id = id if id else uuid4().hex
		self.address = address
		self.port = port
		self.method = method
		self.path, *querystring = uri.split('?', 1)
		if parameters:
			Parameters = CreateDataClass('Parameters', parameters)
			self.params = ToDataClass(parameters, Parameters)
		else:
			self.params = None
		self.qs_ = querystring[0] if len(querystring) else None
		args = parse_qs(self.qs_, keep_blank_values=True) if self.qs_ else {}
		for k, v in args.items():
			if len(v) == 0:
				args[k] = None
			elif len(v) == 1:
				args[k] = unquote(v[0]) if v[0] is not None else None
			else:
				for i, o in enumerate(v):
					v[i] = unquote(o) if o is not None else None
				args[k] = v
		Querystring = CreateDataClass('Querystring', args)
		self.args = ToDataClass(args, Querystring)
		self.props = {}
		for k, v in headers.items() if headers else []:
			self.header(k, v)
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
		return self.qs_

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
	def qs(self) -> Optional[object]:
		return self.args

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
