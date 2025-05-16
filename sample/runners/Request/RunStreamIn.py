# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import *
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
			'Content-Type': IsString(),
			'Content-Length': IsString(ToInteger()),
		},
		requires=('Content-Type', 'Content-Length'),
		format={
			'Content-Type': String(),
			'Content-Length': Integer(),
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
