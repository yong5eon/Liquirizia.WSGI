# -*- coding: utf-8 -*-

from .Request import Request
from .RequestReader import RequestReader
from abc import ABCMeta, abstractmethod
from typing import Any

__all__ = (
	'ContentReader',
	'TypeReader',
)


class ContentReader(metaclass=ABCMeta):
	"""Content Reader Interface"""
	@abstractmethod
	def __call__(self, request: Request, reader: RequestReader) -> Any:
		raise NotImplemented('{} must be implemented __call__'.format(self.__class__.__name__))


class TypeReader(metaclass=ABCMeta):
	"""Type Reader Interface"""
	@abstractmethod
	def __call__(self, o: Any) -> Any:
		raise NotImplemented('{} must be implemented __call__'.format(self.__class__.__name__))
