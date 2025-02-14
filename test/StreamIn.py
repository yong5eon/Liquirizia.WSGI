# -*- coding: utf-8 -*-

from Liquirizia.Test import *
from Liquirizia.WSGI.Test import (
	TestRequest,
	TestRequestStream,
	TestRequestStreamCallback,
)

from Liquirizia.WSGI import (
	Application, 
	Configuration,
	CORS,
	Handler,
	Error,
	Request,
	Response,
	RequestReader,
	ResponseWriter,
)
from Liquirizia.WSGI.Properties import RequestStreamRunner, RequestProperties
from Liquirizia.WSGI.Responses import *


from traceback import format_tb
from time import sleep


@RequestProperties(
	method='PUT',
	url='/stream',
	cors=CORS(),
)
class RunPutStream(RequestStreamRunner):
	def __init__(self, request: Request):
		self.request = request
		return
	def run(self, reader: RequestReader, writer: ResponseWriter):
		if not self.request.size:
			response = ResponseBadRequest('본문의 길이가 없습니다.', format='text/plain', charset='utf-8')
			writer.response(response)
			return
		headers = {
			'Content-Type': '{}{}'.format(self.request.format, '; charset={}'.format(self.request.charset) if self.request.charset else ''),
			'Content-Length': str(self.request.size),
		}
		writer.send(200, 'OK', headers=headers)
		size = self.request.size
		buffer = bytearray()
		while True:
			data = reader.read(size)
			if not data:
				continue
			writer.write(data)
			size -= len(data)
			buffer += data
			if size <= 0:
				break
			sleep(0)
		return

class TestPutStream(Case):
	@Order(0)
	def testOptions(self):
		_ = TestRequest(Application(conf=Configuration()))
		response = _.request(
			method='OPTIONS',
			uri='*'
		)
		ASSERT_IS_EQUAL(response.status, 204)
		ASSERT_TRUE('PUT' in response.header('Allow'))
		response = _.request(
			method='OPTIONS',
			uri='/stream'
		)
		ASSERT_IS_EQUAL(response.status, 204)
		ASSERT_TRUE('PUT' in response.header('Allow'))
		return

	@Order(1)
	def testRequest(self):
		class Callback(TestRequestStreamCallback):
			def __call__(self, testRequestStream):
				for i in range(0, 10):
					testRequestStream.write(str(i).encode('utf-8'))
					sleep(0.1)
				return
		_ = TestRequestStream(Application(conf=Configuration()))
		response = _.send(
			method='PUT',
			uri='/stream',
			headers={
				'Content-Type': 'text/plain; charset=utf-8',
				'Content-Length': str(10),
			},
			cb=Callback(),
		)
		ASSERT_IS_EQUAL(response.status, 200)
		ASSERT_IS_EQUAL(response.buffer.read(), b'0123456789')
		return
