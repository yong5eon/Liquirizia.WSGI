# -*- coding: utf-8 -*-

__all__ = (
	'Encoder'
)


class Encoder(object):
	def headers(self):
		raise NotImplementedError('{} must be implemented headers'.format(self.__class__.__name__))

	def encode(self):
		raise NotImplementedError('{} must be implemented encode'.format(self.__class__.__name__))
