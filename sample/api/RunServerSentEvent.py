# -*- coding: utf-8 -*-

from Liquirizia.WSGI import RequestProperties, Request, RequestReader
from Liquirizia.WSGI.Extends import ServerSentEvents
from Liquirizia.WSGI.Properties import RequestServerSentEventsRunner
from Liquirizia.WSGI.Description import *

from time import sleep
from random import randrange

from traceback import format_tb

__all__ = (
	'RunServerSentEvent'
)

@RequestProperties(
	method='GET',
	url='/api/run/stream/sse',
	description=Description(
		description='1초 간격으로 0에서 1000사이의 랜덤한 숫자를 송출',
		summary='서버 전송 이벤트 샘플',
		tags='RequestServerSentEventsRunner',
		responses=(
			DescriptionResponse(
				status=200,
				description='완료',
				body=DescriptionResponseBody(
					format='text/event-stream',
					example='data:1\ndata:2\ndata:3\n',
				),
			),
		),
	),
)
class RunServerSentEvent(RequestServerSentEventsRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self, writer: ServerSentEvents):
		try:
			writer.begin()
			while True:
				i = randrange(1, 1000)
				writer.emit(data=str(i), id=str(i))
				if i % 5 == 0:
					writer.retry(1000)
				sleep(1)
			writer.end()
		except Exception as e:
			tb =	str(e)
			tb += '\n'
			for line in ''.join(format_tb(e.__traceback__)).strip().split('\n'):
				tb += line
				tb += '\n'
			print(tb)
		return
