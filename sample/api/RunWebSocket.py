# -*- coding: utf-8 -*-

from Liquirizia.WSGI import RequestProperties
from Liquirizia.WSGI.Extends import WebSocket
from Liquirizia.WSGI.Properties import RequestWebSocketRunner
from Liquirizia.WSGI.Description import *

__all__ = (
	'RunWebSocket'
)

@RequestProperties(
	method='GET',
	url='/api/run/socket',
	description=Description(
		description='소켓으로 받은 요청을 그대로 송출',
		summary='웹 소켓 샘플',
		tags='RequestWebSocketRunner',
		responses=(
			DescriptionResponse(
				status=101,
				description='프로토콜 전환',
			),
		),
	),
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
