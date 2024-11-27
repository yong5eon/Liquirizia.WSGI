# -*- coding: utf-8 -*-

from .CORS import CORS

from typing import Dict

__all__ = ('Configuration')


class Configuration(object):
	"""WSGI Application Configuration"""
	def __init__(
		self,
		headers: Dict[str, str] = None,
		cors: CORS = CORS(),
	) -> None:
		self.headers = headers 
		self.cors = cors
		return
	
	def toHeaderName(self, key) -> str:
		if not self.headers:
			return key
		if not isinstance(self.headers, dict):
			return key
		return self.headers.get(key, key)
