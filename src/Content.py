# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from typing import List, Tuple

__all__ = (
	'Content'
)


class Content(metaclass=ABCMeta):
	@abstractmethod
	def headers(self) -> List[Tuple[str, str]]:
		raise NotImplemented('{} must be implemented headers'.format(self.__class__.__name__))
	@property
	@abstractmethod
	def body(self) -> bytes:
		raise NotImplemented('{} must be implemented body'.format(self.__class__.__name__))
	@property
	@abstractmethod
	def format(self) -> str:
		raise NotImplemented('{} must be implemented format'.format(self.__class__.__name__))
	@property
	@abstractmethod
	def charset(self) -> str:
		raise NotImplemented('{} must be implemented format'.format(self.__class__.__name__))

