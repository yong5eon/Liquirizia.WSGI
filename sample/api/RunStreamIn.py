# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import RequestProperties, RequestStreamRunner
from Liquirizia.WSGI import RequestReader, ResponseWriter
from Liquirizia.WSGI.Responses import (
	ResponseBadRequest,
	ResponseBuffer,
)
from Liquirizia.WSGI.Description import *


__all__ = (
	'RunStreamIn'
)


@RequestDescription(
	summary='입력 스트림 샘플',
	description='클라이언트에서 스트림으로 입력한 값을 그대로 반환',
	tags='RequestStreamRunner',
	responses=(
		DescriptionResponse(
			status=200,
			description='완료',
			body=DescriptionResponseBody(
				format='*/*',
			),
		),
	),
)
@RequestProperties(
	method='PUT',
	url='/api/run/stream/in',
)
class RunStreamIn(RequestStreamRunner):
	def __init__(self, request):
		self.request = request
		return

	def run(self, reader: RequestReader, writer: ResponseWriter):
		if not self.request.size:
			response = ResponseBadRequest('본문의 길이가 없습니다.', format='text/plain', charset='utf-8')
			writer.response(response)
			return
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
