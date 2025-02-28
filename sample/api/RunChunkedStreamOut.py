# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import (
	RequestStreamProperties,
	RequestStreamRunner,
)
from Liquirizia.WSGI import Request, RequestReader, ResponseWriter
from Liquirizia.WSGI.Extends import ChunkedStreamWriter
from Liquirizia.WSGI.Description import *

from Liquirizia.Serializer import SerializerHelper

from time import sleep

__all__ = (
	'RunChunkedStreamOut'
)

@RequestDescription(
	summary='청크드 출력 스트림 샘플',
	description='1초 간격으로 0에서 9까지 송출',
	tags='RequestStreamRunner - Chunked',
	responses=(
		Response(
			status=200,
			description='완료',
			content=Content(
				format='text/plain',
				example='0123456789',
			),
		),
	),
)
@RequestStreamProperties(
	method='GET',
	url='/api/run/stream/chunked/out',
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
