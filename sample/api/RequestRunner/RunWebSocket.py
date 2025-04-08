# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import *
from Liquirizia.WSGI.Decoders import *
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Errors import *
from Liquirizia.WSGI import	Request
from Liquirizia.WSGI.Extends import WebSocket

__all__ = (
	'RunWebSocket'
)


@RequestWebSocketProperties(
	method='GET',
	url='/api/run/socket',
	description='소켓으로 받은 요청을 그대로 송출',
	tags='RequestWebSocketRunner',
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
