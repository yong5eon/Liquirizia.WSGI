# -*- coding: utf-8 -*-

from .CORS import CORS

from typing import List, Dict

__all__ = ('Configuration')


class Configuration(object):

	METHODS = [
		'OPTIONS',
		'GET',
		'POST',
		'PUT',
		'DELETE',
		# 'HEAD',
		# 'CONNECT',
		# 'PATCH',
		# 'TRACE',
	]
	ORIGIN = [
		'*',
	]
	HEADERS = [
		'Accept',
		'Accept-Language',
		'Authorization',
		'Content-Language',
		'Content-Length',
		'Content-Type',
	]
	EXPOSE_HEADERS = [
		'*'
	]

	def __init__(
		self,
		envToHeaders: Dict[str, str] = None,
		allowedMethods: List[str] = None,
		cors: CORS = CORS(
			origin=ORIGIN,
			headers=HEADERS,
			exposeHeaders=EXPOSE_HEADERS,
		),
	) -> None:
		self.headers = envToHeaders 
		self.methods = allowedMethods if allowedMethods else self.METHODS
		self.cors = cors
		return
	
	def toHeaderName(self, key) -> str:
		if not self.headers:
			return key
		if not isinstance(self.headers, dict):
			return key
		return self.headers.get(key, key)
