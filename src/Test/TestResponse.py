# -*- coding: utf-8 -*-

from ..Util import ToHeaderName

from .Sender import Sender

from Liquirizia.Serializer import SerializerHelper

from io import BytesIO
from cgi import parse_header

from typing import Iterable

__all__ = (
	'TestResponse',
	'TestResponseServerSentEvents',
	'ServerSentEvent',
)


class TestResponse(object):
	def __init__(
		self,
		sender: Sender,
	):
		self.status = int(sender.status)
		self.message = sender.message
		self.headers = {}
		for k, v in sender.headers:
			args, kwargs = parse_header(v)
			self.headers[ToHeaderName(k)] = {
				'expr': str(v),
				'args': args.split(','),
				'kwargs': kwargs
			}
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
			self.body = SerializerHelper.Decode(
				buffer,
				self.format,
				self.charset
			) if sender.buffer else None
		else:
			self.body = SerializerHelper.Decode(
				sender.buffer,
				self.format,
				self.charset
			) if sender.buffer else None
		return

	def header(self, key: str):
		if key not in self.headers:
			return None
		return self.headers[key]['expr']
	
	@property
	def size(self):
		if 'Content-Length' not in self.headers.keys():
			return 0
		return int(self.headers['Content-Length']['expr'])

	@property
	def format(self):
		if 'Content-Type' not in self.headers.keys():
			return None
		return self.headers['Content-Type']['args'][0]

	@property
	def charset(self):
		if 'Content-Type' not in self.headers.keys():
			return None
		if 'charset' not in self.headers['Content-Type']['kwargs'].keys():
			return None
		return self.headers['Content-Type']['kwargs']['charset']
	

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
			args, kwargs = parse_header(v)
			self.headers[ToHeaderName(k)] = {
				'expr': str(v),
				'args': args.split(','),
				'kwargs': kwargs
			}
		self.buffer = sender.buffer
		return

	def events(self) -> Iterable[ServerSentEvent]:
		# TODO : return parsed event stream buffer to events(data, id, event)
		from io import BufferedReader	
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
