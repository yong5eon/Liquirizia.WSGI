# -*- coding: utf-8 -*-

from .Sender import Sender
from .TestResponse import TestResponse

from ..Application import Application

from urllib.parse import urlencode, quote
from sys import stderr
from io import BytesIO, BufferedReader

from typing import Any, Dict, List, Tuple

__all__ = (
	'TestRequest',
)


class TestRequest(object):
	def __init__(
		self,
		application: Application,
		env: Dict[str, Any] = None,
	):
		self.application = application
		self.env = env
		return
	
	def request(
		self,
		method: str,
		uri: str, 
		qs: Dict = None,
		headers: Dict = None,
		body: Any = None,
		format: str = None,
		charset: str = None,
		version: Tuple[int, int] = (1, 0),
	) -> TestResponse:
		env = {
			'GATEWAY_INTERFACE': 'WSGI',
			'REQUEST_METHOD': method,
			'SCRIPT_NAME': uri,
			'PATH_INFO': uri,
			'QUERY_STRING': urlencode(qs) if qs else None,
			'RAW_URI': '{}{}'.format(quote(uri), '?{}'.format(urlencode(qs)) if qs else ''),
			'CONTENT_TYPE': '{}{}'.format(format, '; charset={}'.format(charset) if charset else '') if format else None,
			'CONTENT_LENGTH': len(body) if body else None,
			'SERVER_NAME': '127.0.0.1',
			'SERVER_PORT': '80',
			'SERVER_PROTOCOL': 'HTTP',
			'SERVER_SOFTWARE': 'Liquirizia(WSGI)',
			'REMOTE_HOST': '127.0.0.1',
			'REMOTE_ADDR': '127.0.0.1',
			'REMOTE_PORT': '65535',
			# 'REMOTE_USER': '',
			# 'AUTH_TYPE': '',
			'wsgi.version': version,
			'wsgi.url_scheme': 'http',
			'wsgi.input': BufferedReader(BytesIO(body)),
			'wsgi.errors': stderr,
			'wsgi.multithread': False,
			'wsgi.multiprocess': False,
		}
		for k, v in self.env if self.env else []:
			env[k] = v
		for k, v in headers.items() if headers else []:
			env['HTTP_' + k.upper().replace('-', '_')] = v
		sender = Sender()
		self.application(env, send=sender)
		return TestResponse(sender)
