# -*- coding: utf-8 -*-

from ..Request import Request

from ..Extends import WebSocket

from abc import ABCMeta, abstractmethod

__all__ = (
	'RequestWebSocketRunner',
)


class RequestWebSocketRunner(metaclass=ABCMeta):
	"""Request WebSocket Runner Interface for Web Socket"""

	@abstractmethod
	def __init__(self, request: Request):
		raise NotImplementedError('{} must be implemented __init__'.format(self.__class__.__name__))
	
	@abstractmethod
	def switch(self, protocol: str) -> bool:
		raise NotImplementedError('{} must be implemented switch'.format(self.__class__.__name__))

	@abstractmethod
	def run(self, ws: WebSocket, op, buffer):
		raise NotImplementedError('{} must be implemented run'.format(self.__class__.__name__))
