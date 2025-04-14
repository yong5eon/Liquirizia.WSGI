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
from Liquirizia.WSGI.Description import Response, Content
from Liquirizia.Description import *

from time import sleep

__all__ = (
	'RunStreamOut'
)

@RequestStreamProperties(
	method='GET',
	url='/api/run/stream',
	response=Response(
		status=200,
		description='OK',
		content=Content(
			format='text/plain',
			schema=String(),
			example='0123456789'
		),
		headers={
			'Content-Type': String(),
			'Content-Length': Integer(),
		},
	),
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
