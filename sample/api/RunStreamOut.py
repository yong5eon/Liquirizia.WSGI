# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import RequestProperties, RequestStreamRunner
from Liquirizia.WSGI import Request, RequestReader, ResponseWriter
from Liquirizia.WSGI.Description import *

from time import sleep

__all__ = (
	'RunStreamOut'
)

@RequestDescription(
	description='1초 간격으로 0에서 9까지 송출',
	summary='출력 스트림 샘플',
	tags='RequestStreamRunner',
	responses=(
		DescriptionResponse(
			status=200,
			description='완료',
			body=DescriptionResponseBody(
				format='text/plain',
				example='0123456789',
			),
		),
	),
)
@RequestProperties(
	method='GET',
	url='/api/run/stream/out',
)
class RunStreamOut(RequestStreamRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self, reader: RequestReader, writer: ResponseWriter):
		headers = {
			'Content-Type': 'text/plain; charset=utf-8',
			'Content-Length': str(10),
		}
		writer.send(200, 'OK', headers=headers)
		for i in range(0, 10):
			writer.write(str(i).encode('utf-8'))
			sleep(1)
		return
