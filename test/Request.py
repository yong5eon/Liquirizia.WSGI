# -*- coding: utf-8 -*-

from ast import Is, Or
from typing import Text
from Liquirizia.Test import *
from Liquirizia.WSGI.Test import TestRequest

from Liquirizia.WSGI import Application
from Liquirizia.WSGI import Request, Response
from Liquirizia.WSGI.Properties import (
	RequestRunner,
	RequestProperties,
	Body,
	FormUrlEncodedContentReader,
	JavaScriptObjectNotationContentReader,
	TextContentReader,
	ByteStringContentReader,
)
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Encoders import JavaScriptObjectNotationEncoder
from Liquirizia.Validator.Patterns import *

from dataclasses import asdict
from json import loads


@RequestProperties(
	method='METHOD',
	url='/:a/:b',
)
class RunRequest(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self) -> Response:
		return ResponseOK()


@RequestProperties(
	method='METHOD',
	url='/json',
	body=Body(
		reader=JavaScriptObjectNotationContentReader(va=IsObject()),
	)
)
class RunRequestJavaScriptObjectNotation(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return
	def run(self, **kwargs) -> Response:
		return ResponseJSON(kwargs)


@RequestProperties(
	method='METHOD',
	url='/bytes',
	body=Body(
		reader=ByteStringContentReader(va=IsByteString()),
	)
)
class RunRequestByteString(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return
	def run(self, buffer: bytes) -> Response:
		return ResponseBuffer(
			status=200,
			buffer=buffer,
			size=len(buffer),
			format=self.request.header('Content-Type').format,
			charset=self.request.header('Content-Type').charset,
		)


@RequestProperties(
	method='METHOD',
	url='/text',
	body=Body(
		reader=TextContentReader(va=IsString()),
	)
)
class RunRequestText(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self, text: str) -> Response:
		return ResponseText(
			status=200,
			text=text,
		)


@RequestProperties(
	method='METHOD',
	url='/form',
	body=Body(
		reader=FormUrlEncodedContentReader(va=IsObject()),
	)
)
class RunRequestForm(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self, **kwargs) -> Response:
		return ResponseJSON(kwargs)


class Request(Case):
	@Order(0)
	def testOptions(self):
		_ = TestRequest(Application())
		response = _.request(
			method='OPTIONS',
			uri='*',
		)
		ASSERT_TRUE(response.status in (200, 204))
		ASSERT_TRUE('METHOD' in response.header('Allow'))
		response = _.request(
			method='OPTIONS',
			uri='/1/2'
		)
		ASSERT_TRUE(response.status in (200, 204))
		ASSERT_TRUE('METHOD' in response.header('Allow'))
		ASSERT_TRUE('METHOD' in response.header('Access-Control-Allow-Methods'))
		return

	@Order(1)	
	def testNotFound(self):
		_ = TestRequest(Application())
		response = _.request(
			method='METHOD',
			uri='/'
		)
		ASSERT_IS_EQUAL(response.status, 404)
		return
	
	@Order(2)
	def testRequest(self):
		_ = TestRequest(Application())
		response = _.request(
			method='METHOD',
			uri='/1/2',
		)
		ASSERT_IS_EQUAL(response.status, 200)
		return

	@Order(3)
	def testRequestJavaScriptObjectNotation(self):
		_ = TestRequest(Application())
		encode = JavaScriptObjectNotationEncoder('utf-8')
		response = _.request(
			method='METHOD',
			uri='/json',
			body=encode({'a': 1, 'b': 2.0, 'c': 'abc'}),
			format='application/json',
			charset='utf-8',
		)
		ASSERT_IS_EQUAL(response.status, 200)
		o = loads(response.body.decode(response.header('Content-Type').charset))
		ASSERT_IS_EQUAL(o, {
			'a': 1,
			'b': 2.0,
			'c': 'abc',
		})
		return

	@Order(4)
	def testRequestByteString(self):
		_ = TestRequest(Application())
		response = _.request(
			method='METHOD',
			uri='/bytes',
			body=b'Hello, World!',
			format='application/octet-stream',
			charset='utf-8',
		)
		ASSERT_IS_EQUAL(response.status, 200)
		ASSERT_IS_EQUAL(response.body, b'Hello, World!')
		ASSERT_IS_EQUAL(response.header('Content-Type').format, 'application/octet-stream')
		ASSERT_IS_EQUAL(response.header('Content-Type').charset, 'utf-8')
		return
	
	@Order(5)
	def testRequestText(self):
		_ = TestRequest(Application())
		response = _.request(
			method='METHOD',
			uri='/text',
			body='Hello, World!'.encode('utf-8'),
			format='text/plain',
			charset='utf-8',
		)
		ASSERT_IS_EQUAL(response.status, 200)
		ASSERT_IS_EQUAL(response.body.decode('utf-8'), 'Hello, World!')
		ASSERT_IS_EQUAL(response.header('Content-Type').format, 'text/plain')
		ASSERT_IS_EQUAL(response.header('Content-Type').charset, 'utf-8')
		return

	@Order(6)
	def testRequestForm(self):
		_ = TestRequest(Application())
		response = _.request(
			method='METHOD',
			uri='/form',
			body='a=1&b=2.0&c=abc'.encode('utf-8'),
			format='application/x-www-form-urlencoded',
			charset='utf-8',
		)
		ASSERT_IS_EQUAL(response.status, 200)
		o = loads(response.body.decode(response.header('Content-Type').charset))
		ASSERT_IS_EQUAL(o, {
			'a': '1',
			'b': '2.0',
			'c': 'abc',
		})
		return