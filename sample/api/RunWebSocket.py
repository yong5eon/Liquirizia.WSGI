# -*- coding: utf-8 -*-

from Liquirizia.WSGI import Request, RequestProperties
from Liquirizia.WSGI.Extends import WebSocket
from Liquirizia.WSGI.Properties import RequestWebSocketRunner

__all__ = (
	'RunWebSocket'
)

@RequestProperties(
	method='GET',
	url='/api/run/socket'
)
class RunWebSocket(RequestWebSocketRunner):
	def __init__(self, request):
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
