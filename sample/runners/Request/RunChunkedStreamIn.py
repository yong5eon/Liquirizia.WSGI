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
from Liquirizia.WSGI.Extends import ChunkedStreamReader
from Liquirizia.WSGI.Description import Response, Content
from Liquirizia.Validator.Patterns import *
from Liquirizia.Description import *

__all__ = (
	'RunChunkedStreamIn'
)


@RequestStreamProperties(
	method='PUT',
	url='/api/run/stream/chunked',
	header=Header(
		{
			'Content-Type': IsString(),
			'Transfer-Encoding': IsString(IsEqualTo('chunked')),
		},
		requires=('Content-Type', 'Transfer-Encoding'),
		format={
			'Content-Type': String(),
			'Transfer-Encoding': String(default='chunked', enum=('Chunked',)),
		}
	),
	response=Response(
		status=200,
		description='성공',
		content=Content(
			format='*/*',
			schema=Binary('본문'),
		),
		headers={
			'Content-Type': String(),
			'Content-Length': Integer(),
		},
	),
	description='클라이언트에서 스트림으로 입력한 값을 그대로 반환',
	tags='RequestStreamRunner - Chunked',
)
class RunChunkedStreamIn(RequestStreamRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self, reader: RequestReader, writer: ResponseWriter):
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
