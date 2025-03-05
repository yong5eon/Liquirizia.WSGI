# -*- coding: utf-8 -*-

from ..Utils import ToHeader, ParseHeader

from .Sender import Sender
from ..Decoder import Decoder
from ..Decoders import (
	TextDecoder,
	JavaScriptObjectNotationDecoder,
)

from io import BytesIO, BufferedReader

from typing import Iterable, Sequence

__all__ = (
	'TestResponse',
	'TestResponseStream',
	'TestResponseServerSentEvents',
	'ServerSentEvent',
)


class TestResponse(object):
	def __init__(
		self,
		sender: Sender,
		decoders: Sequence[Decoder] = (
			TextDecoder('utf-8'),
			JavaScriptObjectNotationDecoder('utf-8'),
		)
	):
		self.status = int(sender.status)
		self.message = sender.message
		self.headers = {}
		for k, v in sender.headers:
			self.headers[k] = str(v) 
		decode = None
		for decoder in decoders:
			if decoder.format == self.format:
				decode = decoder
				break
		if sender.buffer and not decode:
			raise ValueError('Decoder not found')
		if self.header('Transfer-Encoding') == 'chunked':
			buffer = bytes()
			buf = BytesIO(sender.buffer)
			while True:
				line = buf.readline()
				size = int(line, 16)
				if not size:
					break
				buffer += buf.read(size)
				line = buf.readline()
			self.body = decode(buffer) if sender.buffer else None
		else:
			self.body = decode(sender.buffer) if sender.buffer else None
		return

	def header(self, key: str):
		if key not in self.headers:
			return None
		return ParseHeader(key, self.headers[key])
	
	@property
	def size(self):
		_ = self.header('Content-Length')
		if not _: return 0
		return _

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


class TestResponseStream(TestResponse):
	def __init__(self, sender):
		self.status = int(sender.status)
		self.message = sender.message
		self.headers = {}
		for k, v in sender.headers:
			self.headers[k] = v
		self.buffer = sender.buffer
		return

	def read(self, size: int = -1):
		return self.buffer.read(size)
	
	def readline(self, size: int = -1):
		return self.buffer.readline(size)

	def chunk(self):
		line = self.buffer.readline()
		if not line:
			return None
		size = int(line, 16)
		if not size:
			return None
		buffer = self.buffer.read(size)
		line = self.buffer.readline()
		return buffer

	
class ServerSentEvent(object):
	def __init__(
		self,
		id: str = None,
		event: str = None,
		data: str = None,
	):
		self.id = id
		self.event = event
		self.data = data
		return
	

class TestResponseServerSentEvents(TestResponse):
	def __init__(self, sender):
		self.status = int(sender.status)
		self.message = sender.message
		self.headers = {}
		for k, v in sender.headers:
			self.headers[k] = v
		self.buffer = sender.buffer
		return

	def events(self) -> Iterable[ServerSentEvent]:
		reader = BufferedReader(BytesIO(self.buffer))
		events = []
		event = ServerSentEvent()
		while True:
			line = reader.readline().decode('utf-8')
			if not line:
				break
			line = line[:-2]
			try:
				key, value = line.split(': ', maxsplit=1)
				if key == 'id':
					event.id = value
				if key == 'event':
					event.event = value
				if key == 'data':
					event.data = value
			except:
				events.append(event)
				event = ServerSentEvent()
		return events
