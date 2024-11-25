# -*- coding: utf-8 -*-

from Liquirizia.Test import *

from Liquirizia.WSGI import (
		Application, 
		Configuration,
		CORS,
)

from Liquirizia.WSGI import (
	RequestProperties,
	Request,
	Response,
	RequestReader,
	ResponseWriter,
)
from Liquirizia.WSGI.Properties import RequestStreamRunner
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Extends import ChunkedStreamWriter

from Liquirizia.WSGI.Test import TestRequest

from Liquirizia.Serializer import SerializerHelper

from time import sleep


@RequestProperties(
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
			uri='/stream/chunked'
		)
		ASSERT_IS_EQUAL(response.status, 204)
		ASSERT_IS_EQUAL('GET' in response.header('Allow').split(', '), True)
		return

	@Order(1)
	def testRequest(self):
		_ = TestRequest(Application(conf=Configuration()))
		response = _.request(
			method='GET',
			uri='/stream/chunked',
		)
		ASSERT_IS_EQUAL(response.status, 200)
		ASSERT_IS_EQUAL(response.header('Transfer-Encoding'), 'chunked')
		ASSERT_IS_EQUAL(response.body, '0123456789')
		return
