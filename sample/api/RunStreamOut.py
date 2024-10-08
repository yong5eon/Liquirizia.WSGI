# -*- coding: utf-8 -*-

from Liquirizia.WSGI import RequestProperties, Request, RequestReader, ResponseWriter
from Liquirizia.WSGI.Properties import RequestStreamRunner

from Liquirizia.WSGI.Responses import ResponseOK

from time import sleep

__all__ = (
	'RunStreamOut'
)

@RequestProperties(
	method='GET',
	url='/api/run/stream/out'
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
