# -*- coding: utf-8 -*-

from .Properties import Properties

from ..Request import Request
from ..Extends import WebSocket

from abc import ABCMeta, abstractmethod

__all__ = (
	'RequestWebSocketRunner',
)


class RequestWebSocketRunner(metaclass=ABCMeta):
	"""Request WebSocket Runner Interface for Web Socket"""

	__properties__: Properties = None

	@abstractmethod
	def __init__(self, request: Request):
		raise NotImplementedError('{} must be implemented __init__'.format(self.__class__.__name__))
	
	@abstractmethod
	def switch(self, protocol: str) -> bool:
		raise NotImplementedError('{} must be implemented switch'.format(self.__class__.__name__))

	@abstractmethod
	def run(self, ws: WebSocket, op: int, buffer: bytes):
		raise NotImplementedError('{} must be implemented run'.format(self.__class__.__name__))
