# -*- coding: utf-8 -*-

from dataclasses import dataclass

__all__ = (
	'Properties',
)


@dataclass
class Properties(object):
	method: str
	url: str
