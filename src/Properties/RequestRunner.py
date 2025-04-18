# -*- coding: utf-8 -*-

from ..Request import Request
from ..Response import Response

from abc import ABCMeta, abstractmethod
from typing import Tuple, Optional

__all__ = (
	'RequestRunner',
	'RequestFilter',
	'ResponseFilter',
)


class RequestRunner(metaclass=ABCMeta):
	"""Request Runner Interface"""
	@abstractmethod
	def __init__(self, request: Request) -> Response:
		raise NotImplementedError('{} must be implemented __init__'.format(self.__class__.__name__))

	@abstractmethod
	def run(self, *args, **kwargs) -> Response:
		raise NotImplementedError('{} must be implemented run'.format(self.__class__.__name__))


class RequestFilter(metaclass=ABCMeta):
	"""Request Filter Interface"""
	@abstractmethod
	def __call__(self, request: Request) -> Tuple[Request, Optional[Response]]:
		raise NotImplementedError('{} must be implemented run'.format(self.__class__.__name__))


class ResponseFilter(metaclass=ABCMeta):
	"""Request Filter Interface"""
	@abstractmethod
	def __call__(self, request: Request, response: Response) -> Response:
		raise NotImplementedError('{} must be implemented run'.format(self.__class__.__name__))
