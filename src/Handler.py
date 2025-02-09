# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from .Request import Request
from .Response import Response
from .Error import Error

from typing import Optional, Dict, Any

__all__ = (
	'Handler'
)


class Handler(metaclass=ABCMeta):
	"""Request Handler Interface"""
	@abstractmethod
	def onRequest(self, request: Request) -> Request:
		raise NotImplementedError('{} must be implemented onRequest'.format(self.__class__.__name__))
	@abstractmethod
	def onRequestResponse(self, request: Request, response: Response) -> Response:
		raise NotImplementedError('{} must be implemented onResponse'.format(self.__class__.__name__))
	@abstractmethod
	def onRequestComplete(self, request: Request) -> None:
		raise NotImplementedError('{} must be implemented onRequestComplete'.format(self.__class__.__name__))
	@abstractmethod
	def onRequestError(self, request: Request, error: Error) -> Response:
		raise NotImplementedError('{} must be implemented onRequestError'.format(self.__class__.__name__))
	@abstractmethod
	def onRequestException(self, request: Request, e: Exception) -> Response:
		raise NotImplementedError('{} must be implemented onRequestException'.format(self.__class__.__name__))
	@abstractmethod
	def onError(self, env: Dict[str, Any], error: Error) -> Response:
		raise NotImplementedError('{} must be implemented onError'.format(self.__class__.__name__))
	@abstractmethod
	def onException(self, env: Dict[str, Any], e: Exception) -> Response:
		raise NotImplementedError('{} must be implemented onException'.format(self.__class__.__name__))
