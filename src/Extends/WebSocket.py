# -*- coding: utf-8 -*-

from ..RequestReader import RequestReader
from ..ResponseWriter import ResponseWriter

from base64 import b64encode
from hashlib import sha1
from struct import pack, unpack

from uuid import uuid4

__all__ = (
	'WebSocket'
)


class WebSocket(object):
	"""Web Socket Class"""
	"""
	+-+-+-+-+-------+-+-------------+-------------------------------+
	|0				   1				   2				   3  |
	|0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1|
	+-+-+-+-+-------+-+-------------+-------------------------------+
	|F|R|R|R| opcode|M| Payload len |	Extended payload length	|
	|I|S|S|S|  (4)  |A|	 (7)	 |			 (16/64)		   |
	|N|V|V|V|	   |S|			 |   (if payload len==126/127)   |
	| |1|2|3|	   |K|			 |							   |
	+-+-+-+-+-------+-+-------------+ - - - - - - - - - - - - - - - +
	|	 Extended payload length continued, if payload len == 127  |
	+ - - - - - - - - - - - - - - - +-------------------------------+
	|					 Payload Data continued ...				|
	+---------------------------------------------------------------+
	"""

	FIN = 0x80
	OPCODE = 0x0f
	MASKED = 0x80
	PAYLOAD_LEN = 0x7f
	PAYLOAD_LEN_EXT16 = 0x7e
	PAYLOAD_LEN_EXT64 = 0x7f

	OPCODE_CONTINUATION = 0x0
	OPCODE_TEXT = 0x1
	OPCODE_BINARY = 0x2
	OPCODE_CLOSE_CONN = 0x8
	OPCODE_PING = 0x9
	OPCODE_PONG = 0xA

	CLOSE_STATUS_NORMAL = 1000
	DEFAULT_CLOSE_REASON = bytes('', encoding='utf-8')

	def __init__(self, reader: RequestReader, writer: ResponseWriter):
		self.reader = reader
		self.writer = writer
		return

	def accept(self, key):
		GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
		hashed = sha1(key.encode() + GUID.encode())
		encoded = b64encode(hashed.digest()).strip()
		return encoded.decode('ASCII')

	def switch(self, accept, protocol=None):
		headers = {
			'Upgrade': 'websocket',
			'Connection': 'Upgrade',
			'Sec-WebSocket-Accept': self.accept(accept),
		}
		if protocol:
			headers['Sec-WebSocket-Protocol'] = protocol
		self.writer.send(101, 'Switching Protocols', headers=headers)
		return
	
	def read(self):
		try:
			b1, b2 = self.reader.read(2)
		except (ConnectionResetError, ConnectionAbortedError, ConnectionError) as e:
			return None, None
		except ValueError as e:
			b1, b2 = 0, 0

		fin = b1 & self.FIN
		opcode = b1 & self.OPCODE
		masked = b2 & self.MASKED
		size = b2 & self.PAYLOAD_LEN

		if opcode == self.OPCODE_CLOSE_CONN:
			return opcode, None

		if not masked:
			return opcode, None

		if size == 126:
			size = unpack('>H', self.reader.read(2))[0]
		elif size == 127:
			size = unpack('>Q', self.reader.read(8))[0]

		masks = self.reader.read(4)

		buffer = bytearray()
		for buf in self.reader.read(size):
			buf ^= masks[len(buffer) % 4]
			buffer.append(buf)

		return opcode, buffer

	def write(self, buffer, opcode=OPCODE_TEXT):
		"""
		Important: Fragmented(=continuation) messages are not supported since
		their usage cases are limited - when we don't know the payload length.
		"""

		header = bytearray()
		size = len(buffer)

		if size <= 125:  # Normal payload
			header.append(self.FIN | opcode)
			header.append(size)
		elif 126 <= size <= 65535:  # Extended payload
			header.append(self.FIN | opcode)
			header.append(self.PAYLOAD_LEN_EXT16)
			header.extend(pack(b'>H', size))
		elif size < 18446744073709551616:  # Huge extended payload
			header.append(self.FIN | opcode)
			header.append(self.PAYLOAD_LEN_EXT64)
			header.extend(pack(b'>Q', size))
		else:
			raise RuntimeError('Message is too big, Consider breaking it into chunks.')

		self.writer.write(bytes(header + buffer))
		return

	def end(self, status=CLOSE_STATUS_NORMAL, reason=DEFAULT_CLOSE_REASON):
		"""
		Send CLOSE to client
		Args:
				status: Status as defined in https://datatracker.ietf.org/doc/html/rfc6455#section-7.4.1
				reason: Text with reason of closing the connection
		"""
		if status < self.CLOSE_STATUS_NORMAL or status > 1015:
			raise Exception(f"CLOSE status must be between 1000 and 1015, got {status}")

		header = bytearray()
		payload = pack(b'!H', status) + reason
		payload_length = len(payload)
		assert payload_length <= 125, "We only support short closing reasons at the moment"

		# Send CLOSE with status & reason
		header.append(self.FIN | self.OPCODE_CLOSE_CONN)
		header.append(payload_length)

		self.writer.write(bytes(header + payload))
		self.writer.write(b'')
		return

	def ping(self, message):
		self.write(message, opcode=self.OPCODE_PING)
		return

	def pong(self, message):
		self.write(message, opcode=self.OPCODE_PONG)
		return

	def run(self, callback):
		while True:
			op, buffer = self.read()
			if not op:
				break
			if op == self.OPCODE_CLOSE_CONN:
				break
			callback(self, op, buffer)
		return
