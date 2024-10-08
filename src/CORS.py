# -*- coding: utf-8 -*-

__all__ = (
	'CORS'
)


class CORS(object):
	"""CORS(Cross Origin Resource Sharing) Class"""

	ORIGIN = ('*',)
	HEADERS = ('Accept', 'Accept-Language', 'Content-Type', 'Content-Language', 'Content-Length')
	EXPOSE_HEADERS = ()
	AGE = None

	def __init__(self, origin=ORIGIN, headers=HEADERS, exposeHeaders=EXPOSE_HEADERS, age=AGE):
		self.origin = list(set(origin))
		self.headers = list(set(headers))
		self.exposeHeaders = list(set(exposeHeaders))
		self.age = age if age else self.__class__.AGE
		return

	def toHeaders(self):
		headers = dict()
		if len(self.origin):
			headers['Access-Control-Allow-Origin'] = ','.join(self.origin)
		if len(self.headers):
			headers['Access-Control-Allow-Headers'] = ','.join(self.headers)
		if len(self.exposeHeaders):
			headers['Access-Control-Expose-Headers'] = ','.join(self.exposeHeaders)
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
