# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import RequestStreamRunner
from Liquirizia.WSGI import (
	RequestStreamProperties,
	Request,
	RequestReader,
	ResponseWriter,
)

from time import sleep

__all__ = (
	'RunStreamOut'
)

@RequestStreamProperties(
	method='GET',
	url='/api/run/stream',
	summary='Sample of Stream Output with GET',
	description='1초 간격으로 0에서 9까지 송출',
	tags='RequestStreamRunner',
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
