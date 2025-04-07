# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from typing import Any

__all__ = (
	'Encoder',
)


class Encoder(metaclass=ABCMeta):
	"""Content Encoder Interface"""
	@abstractmethod
	def __call__(self, body: Any) -> bytes:
		raise NotImplemented('{} must be implemented __call__'.format(self.__class__.__name__))
