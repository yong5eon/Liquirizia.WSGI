# -*- coding: utf-8 -*-

from Liquirizia.Test import *
from Liquirizia.WSGI.Test import (
	TestRequest,
	TestRequestWebSocket,
	TestRequestWebSocketCallback,
)

from Liquirizia.WSGI import (
	Application, 
	Configuration,
	CORS,
	Handler,
	Error,
	Request,
	Response,
)
from Liquirizia.WSGI.Properties import RequestWebSocketRunner, RequestProperties
from Liquirizia.WSGI.Responses import *

from Liquirizia.WSGI.Extends import WebSocket


from time import sleep
from uuid import uuid4
from traceback import format_tb

from typing import List


@RequestProperties(
	method='GET',
	url='/ws',
	cors=CORS(),
)
class RunWebSocket(RequestWebSocketRunner):
	def __init__(self, request: Request):
		self.request = request
		return
	def switch(self, protocol: str):
		return True

	def run(self, ws: WebSocket, op, buffer):
		if op == ws.OPCODE_PING:
			ws.pong(buffer)
		if op == ws.OPCODE_PONG:
			ws.ping(buffer)
		if op == ws.OPCODE_TEXT:
			ws.write(buffer, ws.OPCODE_TEXT)
		if op == ws.OPCODE_BINARY:
			ws.write(buffer, ws.OPCODE_BINARY)
		return


class TestWebSocket(Case):
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
			uri='/ws'
		)
		ASSERT_IS_EQUAL(response.status, 204)
		ASSERT_TRUE('GET' in response.header('Allow'))
		return

	@Order(1)
	def testRequest(self):
		class Callback(TestRequestWebSocketCallback):
			def __init__(self, input: List[bytes]):
				self.input: List[bytes] = input
				self.output: List[bytes] = []
				return
			def __call__(self, testRequestWebSocket):
				for input in self.input:
					testRequestWebSocket.write(input)
					while True:
						op, buffer = testRequestWebSocket.read()
						if not op:
							continue
						if op == testRequestWebSocket.OPCODE_CLOSE_CONN:
							break
						self.output.append(buffer)
						break
				testRequestWebSocket.end()
				return

		cb = Callback([b'123', b'456', b'789'])
		_ = TestRequestWebSocket(Application(conf=Configuration()))
		response = _.send(
			method='GET',
			uri='/ws',
			headers={
				'Sec-WebSocket-Key': uuid4().hex
			},
			cb=cb,
		)
		ASSERT_IS_EQUAL(response.status, 101)
		ASSERT_IS_EQUAL(cb.output[0], b'123')
		ASSERT_IS_EQUAL(cb.output[1], b'456')
		ASSERT_IS_EQUAL(cb.output[2], b'789')
		return
