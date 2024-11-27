# -*- coding: utf-8 -*-

from typing import Sequence

__all__ = (
	'CORS'
)


class CORS(object):
	"""CORS(Cross Origin Resource Sharing) Class"""
	def __init__(
		self,
		origin: Sequence[str] = None,
		headers: Sequence[str] = None,
		exposeHeaders: Sequence[str] = None,
		age: int = None,
		credentials: bool = False,
	):
		self.origin = origin if origin else []
		self.headers = headers if headers else []
		self.exposeHeaders = exposeHeaders if exposeHeaders else []
		self.age = age
		self.credentials = credentials
		return

	def toHeaders(self):
		headers = dict()
		if self.origin:
			headers['Access-Control-Allow-Origin'] = ', '.join(sorted(list(set(self.origin))))
		if self.headers:
			headers['Access-Control-Allow-Headers'] = ', '.join(sorted(list(set(self.headers))))
		if self.exposeHeaders:
			headers['Access-Control-Expose-Headers'] = ', '.join(sorted(list(set(self.exposeHeaders))))
		if self.credentials:
			headers['Access-Control-Allow-Credentials'] = 'true'
		if self.age:
			headers['Access-Control-Max-Age'] = self.age
		return headers

	def addOrigin(self, origin):
		self.origin.append(origin)
		self.origin = list(set(self.origin))
		return

	def addHeader(self, header):
		self.headers.append(header)
		self.headers = list(set(self.headers))
		return

	def addExposeHeader(self, exposeHeader):
		self.exposeHeaders.append(exposeHeader)
		self.exposeHeaders = list(set(self.exposeHeaders))
		return

	def setAge(self, age):
		self.age = age
		return
