# -*- coding: utf-8 -*-

from Liquirizia.WSGI import RequestProperties, RequestReader, ResponseWriter
from Liquirizia.WSGI.Properties import RequestStreamRunner
from Liquirizia.WSGI.Responses import (
	ResponseBadRequest,
	ResponseBuffer,
)


__all__ = (
	'RunStreamIn'
)

@RequestProperties(
	method='PUT',
	url='/api/run/stream/in'
)
class RunStreamIn(RequestStreamRunner):
	def __init__(self, request):
		self.request = request
		return

	def run(self, reader: RequestReader, writer: ResponseWriter):
		if not self.request.size:
			response = ResponseBadRequest('본문의 길이가 없습니다.')
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
