# -*- coding: utf-8 -*-

from Liquirizia.Test import *
from Liquirizia.WSGI.Test import TestRequest, TestRequestStream, TestRequestStreamCallback

from Liquirizia.WSGI import (
	Application, 
	Configuration,
	CORS,
	Handler,
	Error,
	RequestProperties,
	Request,
	Response,
	RequestReader,
	ResponseWriter,
)
from Liquirizia.WSGI.Properties import RequestStreamRunner
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Extends import ChunkedStreamReader, ChunkedStreamWriter

from traceback import format_tb
from time import sleep


class TestHandler(Handler):
	def onOptions(self, env, response):
		print('OPTIONS  : {}, {}'.format(env['PATH_INFO'], str(response)))
		return response
	def onRequest(self, request: Request):
		print('REQUEST	: {}'.format(str(request)))
		return request, None
	def onRequestResponse(self, request: Request, response: Response):
		print('REQUEST RESPONSE : {} - {}'.format(str(response), response.size))
		return response
	def onRequestComplete(self, request: Request):
		print('REQUEST COMPLETE : {}'.format(str(request)))
		return
	def onRequestError(self, request: Request, error: Error):
		print('REQUEST ERROR : {}'.format(str(request)))
		tb =	str(error)
		tb += '\n'
		for line in ''.join(format_tb(error.__traceback__)).strip().split('\n'):
			tb += line
			tb += '\n'
			print(tb)
		return ResponseError(error, body=tb, format='text/plain', charset='utf-8')
	def onRequestException(self, request: Request, e: Exception):
		print('REQUEST EXCEPTION : {}'.format(str(request)))
		tb =	str(e)
		tb += '\n'
		for line in ''.join(format_tb(e.__traceback__)).strip().split('\n'):
			tb += line
			tb += '\n'
		print(tb)
		return ResponseInternalServerError(body=tb, format='text/plain', charset='utf-8')
	def onError(self, env, error: Error):
		print('ERROR : {} - {}'.format(env['PATH_INFO'], str(error)))
		tb =	str(error)
		tb += '\n'
		for line in ''.join(format_tb(error.__traceback__)).strip().split('\n'):
			tb += line
			tb += '\n'
		print(tb)
		return ResponseError(error, body=tb, format='text/plain', charset='utf-8')
	def onException(self, env, e: Exception):
		print('EXCEPTION : {} - {}'.format(env['PATH_INFO'], str(e)))
		tb =	str(e)
		tb += '\n'
		for line in ''.join(format_tb(e.__traceback__)).strip().split('\n'):
			tb += line
			tb += '\n'
		print(tb)
		return ResponseServiceUnavailable(body=tb, format='text/plain', charset='utf-8')


@RequestProperties(
	method='PUT',
	url='/stream/chunked',
)
class RunPutChunkedStream(RequestStreamRunner):
	def __init__(self, request: Request):
		self.request = request
		return
	def run(self, reader: RequestReader, writer: ResponseWriter):
		if not self.request.header('Transfer-Encoding'):
			response = ResponseBadRequest('본문이 청크 형식이 아닙니다.')
			writer.response(response)
			return
		reader = ChunkedStreamReader(reader)
		writer = ChunkedStreamWriter(writer)
		writer.begin(format=self.request.format, charset=self.request.charset)
		while True:
			buffer = reader.chunk()
			if not buffer:
				break
			writer.chunk(buffer)
			sleep(0.1)
		writer.end()
		return
	

class TestPutChunkedStream(Case):
	@Order(0)
	def testOptions(self):
		_ = TestRequest(Application(conf=Configuration()))
		response = _.request(
			method='OPTIONS',
			uri='*'
		)
		ASSERT_IS_EQUAL(response.status, 204)
		ASSERT_IS_EQUAL('PUT' in response.header('Allow').split(', '), True)
		response = _.request(
			method='OPTIONS',
			uri='/stream/chunked'
		)
		ASSERT_IS_EQUAL(response.status, 204)
		ASSERT_IS_EQUAL('PUT' in response.header('Allow').split(', '), True)
		return

	@Order(1)
	def testRequest(self):
		class Callback(TestRequestStreamCallback):
			def __call__(self, testRequestStream):
				for i in range(0, 10):
					testRequestStream.chunk(str(i).encode('utf-8'))
					sleep(0.1)
				testRequestStream.end()
				return
		_ = TestRequestStream(Application(conf=Configuration()))
		response = _.send(
			method='PUT',
			uri='/stream/chunked',
			headers={
				'Content-Type': 'text/plain; charset=utf-8',
				'Content-Length': str(10),
				'Transfer-Encoding': 'chunked',
			},
			cb=Callback(),
		)
		ASSERT_IS_EQUAL(response.status, 200)
		ASSERT_IS_EQUAL(response.chunk(), b'0')
		ASSERT_IS_EQUAL(response.chunk(), b'1')
		ASSERT_IS_EQUAL(response.chunk(), b'2')
		ASSERT_IS_EQUAL(response.chunk(), b'3')
		ASSERT_IS_EQUAL(response.chunk(), b'4')
		ASSERT_IS_EQUAL(response.chunk(), b'5')
		ASSERT_IS_EQUAL(response.chunk(), b'6')
		ASSERT_IS_EQUAL(response.chunk(), b'7')
		ASSERT_IS_EQUAL(response.chunk(), b'8')
		ASSERT_IS_EQUAL(response.chunk(), b'9')
		return
