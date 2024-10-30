# -*- coding: utf-8 -*-

from .Encoder import Encoder
from .Decoder import Decoder

__all__ = (
	'FORMATS',
	'Encoder',
	'Decoder',
)


FORMATS = [
	'application/x-www-form-urlencoded',
	'form-urlencoded',
	'application/x-www-form',
	'form',
]
