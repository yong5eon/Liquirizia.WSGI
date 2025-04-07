# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import RequestStreamRunner
from Liquirizia.WSGI import (
	RequestStreamProperties,
	Request,
	RequestReader,
	ResponseWriter,
)
from Liquirizia.WSGI.Extends import ChunkedStreamReader
from Liquirizia.WSGI.Responses import (
	ResponseBadRequest,
	ResponseBuffer,
)

__all__ = (
	'RunChunkedStreamIn'
)


@RequestStreamProperties(
	method='PUT',
	url='/api/run/stream/chunked',
	summary='청크드 입력 스트림 샘플',
	description='클라이언트에서 스트림으로 입력한 값을 그대로 반환',
	tags='RequestStreamRunner - Chunked',
)
class RunChunkedStreamIn(RequestStreamRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self, reader: RequestReader, writer: ResponseWriter):
		if not self.request.header('Transfer-Encoding'):
			response = ResponseBadRequest('본문이 청크 형식이 아닙니다.')
			writer.response(response)
			return
		reader: ChunkedStreamReader = ChunkedStreamReader(reader)
		data = ''
		while 1:
			chunk = reader.chunk()
			if not chunk:
				break
			data += chunk
		response = ResponseBuffer(data, self.request.format, self.request.charset)
		writer.response(response)
		return
