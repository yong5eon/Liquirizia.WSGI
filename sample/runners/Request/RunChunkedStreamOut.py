# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import *
from Liquirizia.WSGI.Validators import *
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Errors import *
from Liquirizia.WSGI import	(
	Request,
	RequestReader,
	ResponseWriter,
)
from Liquirizia.WSGI.Encoders import *
from Liquirizia.WSGI.Extends import ChunkedStreamWriter
from Liquirizia.WSGI.Description import Response, Content
from Liquirizia.Description import *

from time import sleep

__all__ = (
	'RunChunkedStreamOut'
)


@RequestStreamProperties(
	method='GET',
	url='/api/run/stream/chunked',
	response=Response(
		status=200,
		description='OK',
		content=Content(
			format='text/plain',
			schema=String(),
			example='1\r\n0\r\n1\r\n1\r\n1\r\n2\1\n1\r\n3\r\n1\r\n4\r\n1\r\n5\r\n1\r\n6\r\n1\r\n7\r\n1\r\n8\r\n1\r\n9\r\n'
		),
		headers={
			'Content-Type': String(),
			'Transfer-Encoding': String(default='chunked'),
		},
	),
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
