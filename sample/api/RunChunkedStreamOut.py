# -*- coding: utf-8 -*-

from Liquirizia.WSGI import RequestProperties, Request, RequestReader, ResponseWriter
from Liquirizia.WSGI.Extends import ChunkedStreamWriter
from Liquirizia.WSGI.Properties import RequestStreamRunner

from Liquirizia.Serializer import SerializerHelper

from time import sleep

__all__ = (
	'RunChunkedStreamOut'
)

@RequestProperties(
	method='GET',
	url='/api/run/stream/chunked/out'
)
class RunChunkedStreamOut(RequestStreamRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self, reader: RequestReader, writer: ResponseWriter):
		writer = ChunkedStreamWriter(writer)
		writer.begin(format='text/plain', charset='utf-8')
		for i in range(0, 10):
			writer.chunk(SerializerHelper.Encode(str(i), format='text/plain', charset='utf-8'))
			sleep(1)
		writer.end()
		return
