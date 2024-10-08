# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

__all__ = (
	'Object'
)


class Object(metaclass=ABCMeta):
	"""Multi Part Form Data Object Interface"""

	@abstractmethod
	def headers(self):
		raise NotImplementedError('{} must be implemented headers'.format(self.__class__.__name__))

	@abstractmethod
	def body(self):
		raise NotImplementedError('{} must be implemented body'.format(self.__class__.__name__))
