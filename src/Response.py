# -*- coding: utf-8 -*-

from .Cookie import Cookie
from .Util import ToHeaderName

from http.cookies import SimpleCookie
from cgi import parse_header
from email.utils import formatdate
from time import time

__all__ = (
	'Response'
)


class Response(object):
	"""HTTP Response Class"""

	def __init__(self, status: int, message: str, headers: dict = None, body=None, format=None, charset=None):
		self.status = status
		self.message = message
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
			self.header('Content-Length', len(body) if body else 0)
		self.header('Date', formatdate(time(), usegmt=True))
		self.obj = body
		return

	def __repr__(self):
		return 'Response(status:{}, message:{}, size:{})'.format(
			self.status,
			self.message,
			self.size,
		)
	
	def __str__(self):
		return '{} {}'.format(
			self.status,
			self.message,
		)

	def header(self, key: str, value=None):
		if value is not None:
			# TODO : according to value, use other parse methods
			args, kwargs = parse_header(str(value))
			self.props[ToHeaderName(key)] = {
				'expr': str(value),
				'args': args.split(','),
				'kwargs': kwargs
			}
		else:
			if key not in self.props:
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
			headers.append(('Set-Cookie', cookie.OutputString()))

		return headers

	def cookie(self, name, value, expires=None, path=None, domain=None, secure=None, http=None, version=None, max=None, comment=None):
		self.cookies[name] = Cookie(
			name=name,
			value=value,
			expires=expires,
			path=path,
			domain=domain,
			secure=secure,
			http=http,
			version=version,
			max=max,
			comment=comment
		)
		return

	@property
	def size(self):
		if 'Content-Length' not in self.props.keys():
			return 0
		return int(self.props['Content-Length']['expr'])

	@property
	def format(self):
		if 'Content-Type' not in self.props.keys():
			return None
		return self.props['Content-Type']['args'][0]

	@property
	def charset(self):
		if 'Content-Type' not in self.props.keys():
			return None
		if 'charset' not in self.props['Content-Type']['kwargs'].keys():
			return None
		return self.props['Content-Type']['kwargs']['charset']

	@property
	def body(self):
		return self.obj

	@body.setter
	def body(self, body):
		self.obj = body
		return
