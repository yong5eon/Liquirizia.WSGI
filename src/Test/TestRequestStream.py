# -*- coding: utf-8 -*-

from .Sender import SenderStream, BufferedStream
from .TestResponse import TestResponse, TestResponseStream

from ..Application import Application

from urllib.parse import urlencode, quote
from sys import stderr
from threading import Thread

from abc import ABCMeta, abstractmethod

from typing import Any, Dict, List, Tuple

__all__ = (
	'TestRequestStream',
	'TestRequestStreamCallback',
)


class TestRequestStream(object): pass
class TestRequestStreamCallback(metaclass=ABCMeta):
	@abstractmethod
	def __call__(self, testRequestStream: TestRequestStream):
		pass


class TestRequestStream(object):
	def __init__(
		self,
		application: Application,
		env: Dict[str, Any] = None,
	):
		self.application = application
		self.env = env
		self.sender = SenderStream()
		self.input = BufferedStream()
		return
	
	def send(
		self,
		method: str,
		uri: str, 
		qs: Dict = None,
		headers: Dict = None,
		cb: TestRequestStreamCallback = None,
		version: Tuple[int, int] = (1, 0),
	):
		env = {
			'GATEWAY_INTERFACE': 'WSGI',
			'REQUEST_METHOD': method,
			'SCRIPT_NAME': uri,
			'PATH_INFO': uri,
			'QUERY_STRING': urlencode(qs) if qs else None,
			'RAW_URI': '{}{}'.format(quote(uri), '?{}'.format(urlencode(qs)) if qs else ''),
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
			'wsgi.input': self.input.reader,
			'wsgi.errors': stderr,
			'wsgi.multithread': False,
			'wsgi.multiprocess': False,
		}
		for k, v in self.env if self.env else []:
			env[k] = v
		for k, v in headers.items() if headers else []:
			if k in [
				'Content-Type',
				'Content-Length',
			]:
				env[k.upper().replace('-', '_')] = v
				continue
			env['HTTP_' + k.upper().replace('-', '_')] = v
		if cb:
			thread = Thread(target=cb, args=(self,))
			thread.start()
		self.application(env, send=self.sender)
		self.sender.close()
		return TestResponseStream(self.sender)
	
	def read(self, size: int = -1):
		return self.sender.read(size)
	
	def readline(self, size: int = -1):
		return self.sender.readline(size)
	
	def write(self, buffer: bytes):
		self.input.write(buffer)
		return
	
	def chunk(self, buffer: bytes = None):
		CRLF = '\r\n'
		if buffer:
			size = '{:x}'.format(len(buffer) if buffer else 0)
			self.input.write(size.encode())
			self.input.write(CRLF.encode())
			self.input.write(buffer)
			self.input.write(CRLF.encode())
			return
		else:
			line = self.sender.readline()
			if not line:
				return None
			size = int(line, 16)
			if not size:
				return None
			buffer = self.sender.read(size)
			line = self.sender.readline()
			return buffer
	
	def end(self):
		CRLF = '\r\n'
		size = '{:x}'.format(0)
		self.input.write(size.encode())
		self.input.write(CRLF.encode())
		self.input.write(b'')
		return
