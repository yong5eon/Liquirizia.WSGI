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
from Liquirizia.WSGI.Properties import RequestStreamRunner, RequestStreamProperties
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Extends import ChunkedStreamWriter

from Liquirizia.Serializer import SerializerHelper

from traceback import format_tb
from time import sleep


@RequestStreamProperties(
	method='GET',
	url='/stream/chunked',
)
class RunGetChunkedStream(RequestStreamRunner):
	def __init__(self, request: Request):
		self.request = request
		return
	def run(self, reader: RequestReader, writer: ResponseWriter):
		writer = ChunkedStreamWriter(writer)
		writer.begin(format='text/plain', charset='utf-8')
		for i in range(0, 10):
			writer.chunk(SerializerHelper.Encode(str(i), format='text/plain', charset='utf-8'))
			sleep(0.1)
		writer.end()
		return


class TestGetChunkedStream(Case):
	@Order(0)
	def testOptions(self):
		_ = TestRequest(Application(conf=Configuration()))
		response = _.request(
			method='OPTIONS',
			uri='*'
		)
		ASSERT_IS_EQUAL(response.status, 204)
		ASSERT_TRUE('GET' in response.header('Allow'))
		response = _.request(
			method='OPTIONS',
			uri='/stream/chunked'
		)
		ASSERT_IS_EQUAL(response.status, 204)
		ASSERT_TRUE('GET' in response.header('Allow'))
		return

	@Order(1)
	def testRequest(self):
		class Callback(TestRequestStreamCallback):
			def __init__(self):
				self.output = bytearray()
				return
			def __call__(self, testRequestStream):
				while True:
					buffer = testRequestStream.chunk()
					if not buffer:
						break
					self.output += buffer
				return
		cb = Callback()
		_ = TestRequestStream(Application(conf=Configuration()))
		response = _.send(
			method='GET',
			uri='/stream/chunked',
			cb=cb,
		)
		ASSERT_IS_EQUAL(response.status, 200)
		ASSERT_TRUE('chunked' in response.header('Transfer-Encoding'))
		ASSERT_IS_EQUAL(cb.output, b'0123456789')
		return
