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
from Liquirizia.WSGI.Description import Response, Content
from Liquirizia.Validator.Patterns import *
from Liquirizia.Description import *

__all__ = (
	'RunStreamIn'
)


@RequestStreamProperties(
	method='PUT',
	url='/api/run/stream',
	header=Header(
		{
			'Content-Type': IsString(error=BadRequestError('본문 유형(Content-Type)이 필요합니다.')),
			'Content-Length': IsString(ToInteger(error=BadRequestError('본문 길이(Content-Length)는 정수이어야 합니다.')), error=BadRequestError('본문 길이(Content-Length)가 필요합니다.')),
		},
		requires=('Content-Type', 'Content-Length'),
		requiresError=BadRequestError('헤더에 본문 유형(Content-Type)과 본문 길이(Content-Length)가 필요합니다.'),
		format={
			'Content-Type': String(),
			'Content-Length': Integer(),
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
	tags='RequestStreamRunner',
)
class RunStreamIn(RequestStreamRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self, reader: RequestReader, writer: ResponseWriter):
		size = self.request.size
		buffer = bytearray()
		while True:
			data = reader.read(size)
			print('READ : {} - {}'.format(len(data), data))
			size -= len(data)
			buffer += data
			if size <= 0:
				break
		response = ResponseBuffer(
			buffer=bytes(buffer), 
			size=len(buffer), 
			format=self.request.format, 
			charset=self.request.charset
		)
		writer.response(response)
		return
