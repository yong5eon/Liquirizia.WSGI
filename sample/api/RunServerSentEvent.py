# -*- coding: utf-8 -*-

from Liquirizia.WSGI import RequestProperties, Request, RequestReader
from Liquirizia.WSGI.Extends import ServerSentEvents
from Liquirizia.WSGI.Properties import RequestServerSentEventsRunner

from time import sleep
from random import randrange

from traceback import format_tb

__all__ = (
	'RunServerSentEvent'
)

@RequestProperties(
	method='GET',
	url='/api/run/stream/sse'
)
class RunServerSentEvent(RequestServerSentEventsRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self, writer: ServerSentEvents):
		try:
			writer.begin(charset='utf-8')
			while True:
				i = randrange(1, 1000)
				writer.emit(data=str(i))
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
