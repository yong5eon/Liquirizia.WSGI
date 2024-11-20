# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from .Request import Request
from .Response import Response
from .Error import Error

from typing import Optional

__all__ = (
	'Handler'
)


class Handler(metaclass=ABCMeta):
	"""Request Handler Interface"""
	@abstractmethod
	def onRequest(self, request: Request) -> Optional[Request]:
		raise NotImplementedError('{} must be implemented onRequest'.format(self.__class__.__name__))
	@abstractmethod
	def onRequestResponse(self, request: Request, response: Response) -> Optional[Response]:
		raise NotImplementedError('{} must be implemented onResponse'.format(self.__class__.__name__))
	@abstractmethod
	def onRequestComplete(self, request: Request) -> None:
		raise NotImplementedError('{} must be implemented onRequestComplete'.format(self.__class__.__name__))
	@abstractmethod
	def onRequestError(self, request: Request, error: Error) -> Optional[Response]:
		raise NotImplementedError('{} must be implemented onRequestError'.format(self.__class__.__name__))
	@abstractmethod
	def onRequestException(self, request: Request, e: Exception) -> Optional[Response]:
		raise NotImplementedError('{} must be implemented onRequestException'.format(self.__class__.__name__))
	@abstractmethod
	def onError(self, error: Error) -> Optional[Response]:
		raise NotImplementedError('{} must be implemented onError'.format(self.__class__.__name__))
	@abstractmethod
	def onException(self, e: Exception) -> Optional[Response]:
		raise NotImplementedError('{} must be implemented onException'.format(self.__class__.__name__))
