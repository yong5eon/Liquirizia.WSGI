# -*- coding: utf-8 -*-

__all__ = ('Configuration')


class Configuration(object):
	def __init__(
		self,
		headers: dict = None,
	) -> None:
		self.headers = headers
		return
	
	def toHeaderName(self, key) -> str:
		if not self.headers:
			return key
		if not isinstance(self.headers, dict):
			return key
		return self.headers.get(key, key)