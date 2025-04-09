# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import *
from Liquirizia.WSGI.Properties.Validator import *
from Liquirizia.WSGI.Decoders import *
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
			'Content-Type': IsString(error=BadRequestError('본문 유형(Content-Type)이 필요합니다.')),
			'Transfer-Encoding': IsString(IsEqualTo('chunked', error=BadRequestError('전송방식(Transfer-Encoding)은 chunked 이어야 합니다.')), error=BadRequestError('전송방식(Transfer-Encoding)이 필요합니다.')),
		},
		requires=('Content-Type', 'Transfer-Encoding'),
		requiresError=BadRequestError('헤더에 본문 유형(Content-Type)과 전송 방식(Transfer-Encoding)이 필요합니다.'),
		format={
			'Content-Type': String(),
			'Transfer-Encoding': String(default='chunked', enum=('Chunked',)),
		}
	),
	body=Body(
		format=Binary()
	),
	response=(
		Response(
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
		Response(
			status=400,
			description='잘못된 요청',
			content=Content(
				format='text/plain',
				schema=String('원인'),
			),
		),
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
