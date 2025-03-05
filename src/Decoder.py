# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from typing import Any

__all__ = (
	'Decoder',
)


class Decoder(metaclass=ABCMeta):
	"""Content Decoder Interface"""
	@abstractmethod
	def __call__(self, body: bytes) -> Any:
		raise NotImplemented('{} must be implemented __call__'.format(self.__class__.__name__))
	@property
	@abstractmethod
	def format(self):
		raise NotImplemented('{} must be implemented format'.format(self.__class__.__name__))
	@property
	@abstractmethod
	def charset(self):
		raise NotImplemented('{} must be implemented charset'.format(self.__class__.__name__))
