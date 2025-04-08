# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import RequestStreamRunner
from Liquirizia.WSGI import (
	RequestStreamProperties,
	Request,
	RequestReader,
	ResponseWriter,
)
from Liquirizia.WSGI.Extends import ChunkedStreamWriter
from Liquirizia.WSGI.Encoders import TextEncoder

from time import sleep

__all__ = (
	'RunChunkedStreamOut'
)


@RequestStreamProperties(
	method='GET',
	url='/api/run/stream/chunked',
	summary='Sample of Chunked Stream Output with GET',
	description='1초 간격으로 0에서 9까지 송출',
	tags='RequestStreamRunner - Chunked',
)
class RunChunkedStreamOut(RequestStreamRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self, reader: RequestReader, writer: ResponseWriter):
		writer: ChunkedStreamWriter = ChunkedStreamWriter(writer)
		writer.begin(format='text/plain', charset='utf-8')
		encode = TextEncoder('utf-8')
		for i in range(0, 10):
			writer.chunk(encode(str(i)))
			sleep(1)
		writer.end()
		return
