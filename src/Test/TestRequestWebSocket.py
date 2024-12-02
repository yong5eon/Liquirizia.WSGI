# -*- coding: utf-8 -*-

from .Sender import SenderStream
from .BufferedStream import BufferedStream
from .TestResponse import TestResponseStream

from ..Application import Application

from urllib.parse import urlencode
from sys import stderr
from threading import Thread
from struct import pack, unpack

from abc import ABCMeta, abstractmethod

from typing import Any, Dict, List, Tuple

__all__ = (
	'TestRequestWebSocket',
	'TestRequestWebSocketCallback',
)


class TestRequestWebSocket(object): pass
class TestRequestWebSocketCallback(metaclass=ABCMeta):
	@abstractmethod
	def __call__(self, testRequestWebSocket: TestRequestWebSocket):
		pass


class TestRequestWebSocket(object):

	FIN = 0x80
	OPCODE = 0x0f
	MASKED = 0x80
	PAYLOAD_LEN = 0x7f
	PAYLOAD_LEN_EXT16 = 0x7e
	PAYLOAD_LEN_EXT64 = 0x7f

	OPCODE_CONTINUATION = 0x00
	OPCODE_TEXT = 0x01
	OPCODE_BINARY = 0x02
	OPCODE_CLOSE_CONN = 0x08
	OPCODE_PING = 0x09
	OPCODE_PONG = 0x0a

	CLOSE_STATUS_NORMAL = 1000
	DEFAULT_CLOSE_REASON = bytes('', encoding='utf-8')

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
		cb: TestRequestWebSocketCallback = None,
		version: Tuple[int, int] = (1, 0),
	):
		env = {
			'GATEWAY_INTERFACE': 'WSGI',
			'REQUEST_METHOD': method,
			'SCRIPT_NAME': uri,
			'PATH_INFO': uri,
			'QUERY_STRING': urlencode(qs) if qs else None,
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
		return TestResponseStream(self.sender)
	
	def read(self):
		try:
			b1, b2 = self.sender.read(2)
		except (ConnectionResetError, ConnectionAbortedError, ConnectionError) as e:
			return None, None
		except ValueError as e:
			b1, b2 = 0, 0

		fin = b1 & self.FIN
		opcode = b1 & self.OPCODE
		masked = b2 & self.MASKED
		size = b2 & self.PAYLOAD_LEN

		if opcode == self.OPCODE_CLOSE_CONN:
			return opcode, None

		if size == 126:
			size = unpack('>H', self.sender.read(2))[0]
		elif size == 127:
			size = unpack('>Q', self.sender.read(8))[0]

		if masked:
			masks = self.sender.read(4)
			buffer = bytearray()
			for buf in self.sender.read(size):
				buf ^= masks[len(buffer) % 4]
				buffer.append(buf)
			buffer = bytes(buffer)
		else:
			buffer = self.sender.read(size)

		return opcode, buffer

	def write(self, buffer: bytes, opcode=OPCODE_TEXT):
		"""
		Important: Fragmented(=continuation) messages are not supported since
		their usage cases are limited - when we don't know the payload length.
		"""

		header = bytearray()
		size = len(buffer)

		if size <= 125:  # Normal payload
			header.append(self.FIN | opcode)
			header.append(size)
		elif 126 <= size <= 65535:  # Extended payload
			header.append(self.FIN | opcode)
			header.append(self.PAYLOAD_LEN_EXT16)
			header.extend(pack(b'>H', size))
		elif size < 18446744073709551616:  # Huge extended payload
			header.append(self.FIN | opcode)
			header.append(self.PAYLOAD_LEN_EXT64)
			header.extend(pack(b'>Q', size))
		else:
			raise RuntimeError('Message is too big, Consider breaking it into chunks.')

		self.input.write(bytes(header))
		self.input.write(buffer)
		return

	def end(self, status=CLOSE_STATUS_NORMAL, reason=DEFAULT_CLOSE_REASON):
		"""
		Send CLOSE to client
		Args:
				status: Status as defined in https://datatracker.ietf.org/doc/html/rfc6455#section-7.4.1
				reason: Text with reason of closing the connection
		"""
		if status < self.CLOSE_STATUS_NORMAL or status > 1015:
			raise Exception(f"CLOSE status must be between 1000 and 1015, got {status}")

		header = bytearray()
		payload = pack(b'!H', status) + reason
		payload_length = len(payload)
		assert payload_length <= 125, "We only support short closing reasons at the moment"

		# Send CLOSE with status & reason
		header.append(self.FIN | self.OPCODE_CLOSE_CONN)
		header.append(payload_length)

		self.input.write(bytes(header + payload))
		self.input.write(b'')
		return

	def ping(self, message):
		self.write(message, opcode=self.OPCODE_PING)
		return

	def pong(self, message):
		self.write(message, opcode=self.OPCODE_PONG)
		return
